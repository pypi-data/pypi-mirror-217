#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from past.utils import old_div
from builtins import int
from builtins import str
from builtins import bytes
from builtins import range
import os, sys, time, json, re
from random import randint
from datetime import datetime
try:
    from httplib import BadStatusLine
    from urllib2 import URLError
    from urllib import quote
except ImportError:
    from http.client import BadStatusLine
    from urllib.error import URLError
    from urllib.parse import quote

from ssl import SSLError
import socket
import requests
requests.packages.urllib3.disable_warnings()
from multiprocessing import Process, Event
from gazouilloire.multiprocessing import Queue
from gazouilloire.exports.tweet_fields import TWEET_FIELDS
import signal
import psutil
from twitter import TwitterError, TwitterHTTPError
from pytz import timezone, all_timezones
from math import pi, sin, cos, acos
import shutil
from ebbe.utils import pick
from twitwi import normalize_tweet
from twitwi.constants import FORMATTED_TWEET_DATETIME_FORMAT
from ural.get_domain_name import get_hostname_prefixes
from gazouilloire.database.elasticmanager import ElasticManager, prepare_db, bulk_update
from elasticsearch import helpers, exceptions
from gazouilloire.url_resolve import resolve_loop, count_and_log
from gazouilloire.config_format import load_conf, log
from gazouilloire.twitter_connexion import get_oauth, instantiate_clients

DEPILER_BATCH_SIZE = 5000
RESOLVER_BATCH_SIZE = 5000
STOP_TIMEOUT = 15 # Time (in seconds) before killing the process after a keyboard interrupt.


def get_timestamp(time, locale):
    tim = datetime.strptime(time, '%a %b %d %H:%M:%S +0000 %Y')
    if locale:
        utc_date = timezone('UTC').localize(tim)
        locale_date = utc_date.astimezone(locale)
        return locale_date.timestamp()
    return tim.timestamp()


def breakable_sleep(delay, exit_event):
    t = time.time() + delay
    while time.time() < t and not exit_event.is_set():
        time.sleep(1)


def kill_alive_processes(processes, timeout):
    gone, alive = psutil.wait_procs(processes, timeout=timeout)
    for p in alive:
        log.debug("Killing process nb {}".format(p.pid, ))
        p.kill()


def find_running_processes(pids):
    running_processes = []
    for pid in pids:
        try:
            p = psutil.Process(int(pid))
            if p.status() == "zombie":
                running_processes.append(None)
            running_processes.append(p)
        except psutil.NoSuchProcess:
            running_processes.append(None)
    return running_processes


def get_pids(pidfile, stoplock_file):
    """
    read pidfile and return an iterable of process ids
    """
    try:
        with open(pidfile, 'r') as pf:
            pids = pf.readlines()
        return pids
    except (IOError, IndexError):
        # If reading an existing pidfile crashes, it is corrupted and should be dropped
        if os.path.exists(pidfile):
            os.remove(pidfile)
        # If there is no pidfile but a stoplock exists it is obviously obsolete
        if os.path.exists(stoplock_file):
            os.remove(stoplock_file)
        return []


# Check if stoplock is present, if so remove it when no running_processes or stop here otherwise
def is_already_stopping(pids, stoplock_file, running_processes=None):
    if running_processes is None:
        running_processes = find_running_processes(pids)
    if not running_processes or not any(running_processes):
        os.remove(stoplock_file)
        log.warning(
            "Gazouilloire was currently stopping but all processes were already stopped. .stoplock file was removed.")
        return True
    log.error("Gazouilloire is currently stopping. Please wait before trying to start, restart or stop.")
    sys.exit(1)


def stop(path, timeout=STOP_TIMEOUT):
    """
    Stop the collection
    """
    pidfile = os.path.join(path, '.lock')
    stoplock_file = os.path.join(path, '.stoplock')
    pids = get_pids(pidfile, stoplock_file)

    if os.path.exists(stoplock_file):
        return is_already_stopping(pids, stoplock_file)

    # Indicate that the process is stopping by creating a .stoplock file
    open(stoplock_file, 'w').close()

    # Get the pid from the pidfile
    try:
        pid = int(pids[0].strip()) if pids else None

        if not pid:
           # If an existing pidfile lists no process, it is corrupted and should be dropped
            if os.path.exists(pidfile):
                message = "pidfile %s is corrupted, removing it.\n"
                os.remove(pidfile)
            else:
                message = "pidfile %s does not exist. Daemon not running?\n"
            log.warning(message % pidfile)
            os.remove(stoplock_file)
            return False

        # Kill the processes
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            parent.terminate()
            kill_alive_processes(children, timeout)
        except psutil.NoSuchProcess:
            processes_to_kill = []
            pf = open(pidfile, 'r')
            for pid in pf.readlines():
                try:
                    p = psutil.Process(int(pid))
                    if p.name().startswith("gazou"):
                        processes_to_kill.append(p)
                        p.terminate
                except psutil.NoSuchProcess:
                    continue
            kill_alive_processes(processes_to_kill, timeout)
            pf.close()

        if os.path.exists(pidfile):
            os.remove(pidfile)
        os.remove(stoplock_file)
        return True

    # remove .stoplock file in case of crash
    except Exception as error:
        message = "Some {} occurred while stopping: {}"
        log.error(message.format(type(error), error))
        os.remove(stoplock_file)
        return False


def start_process(process, path):
    pidfile = os.path.join(path, ".lock")
    process.start()
    pid = process.pid
    open(pidfile, 'a').write("%s\n" % pid)


def write_pile(pile, todo, file_prefix):
    store = []
    if pile is not None:
        while not pile.safe_empty():
            store.append(pile.get())
    store.extend(todo)
    if store:
        path = datetime.strftime(datetime.now(), file_prefix +"_%Y%m%d-%H%M.json")
        if not os.path.isdir(os.path.dirname(path)):
            os.mkdir(os.path.dirname(path))
        with open(path, "w") as f:
            json.dump(store, f)
        log.info("Saved {} tweets to {}".format(len(store), path))


def load_pile(path, file_prefix, pile):
    if os.path.isdir(path):
        for file_name in os.listdir(path):
            if file_name.startswith(file_prefix):
                file_path = os.path.join(path, file_name)
                try:
                    with open(file_path, "r") as f:
                        objects = json.load(f)
                        for o in objects:
                            pile.put(o)
                    log.debug("Loaded {} tweets from {}".format(len(objects), file_name))
                except json.decoder.JSONDecodeError as e:
                    log.error("Impossible to open pile file {}, you might want to try and fix it: {}".format(file_name, str(e)))
                    continue
                os.remove(file_path)


def preprocess_tweet_for_indexing(normalized_tweet):
    hostnames = set()
    for hostname in set(normalized_tweet["domains"]):
        hostnames.update(set(get_hostname_prefixes(hostname)))
    normalized_tweet["domains"] = list(hostnames)
    return pick(normalized_tweet, TWEET_FIELDS)


def prepare_tweets(tweets, locale):
    for tweet in tweets:
        if not isinstance(tweet, dict):
            continue
        if "collected_via" not in tweet:
            try:
                for subtweet in normalize_tweet(tweet, locale=locale, extract_referenced_tweets=True):
                    yield preprocess_tweet_for_indexing(subtweet)
            except KeyError as missing_field:
                log.warning("Missing '{}' field in tweet: \n{}".format(missing_field, tweet))
                continue
            except Exception as e:
                log.error("LAST TWEET PROCESSED WAS: %s" % tweet)
                raise e
        else:
            yield tweet


def index_bulk(db, bulk, exit_event, pile_dir, retry=0):
    MAX_RETRIES = 15
    try:
        updated, created, errors = bulk_update(db.client, actions=db.prepare_indexing_tweets(bulk))
        log.debug("Saved {} tweets in database (including {} new ones)".format(updated, created))
        if errors:
            log.error("Warning: {} tweets could not be updated properly in elasticsearch:\n - {}".format(len(errors), "\n -".join(json.dumps(e) for e in errors)))
    except (exceptions.ConnectionError, helpers.errors.BulkIndexError) as e:
        if retry < MAX_RETRIES:
            retry += 1
            if type(e) == helpers.errors.BulkIndexError:
                delay = randint(1, 5)   # Random delay to ensure difference between two concurrent running gazouilloire
            else:
                delay = 5 * retry       # Incremental delay to wait up to 10min before crashing
            log.warning("Could not index bulk of {} tweets because of {}, will retry in {} seconds...".format(len(bulk), type(e), delay))
            breakable_sleep(delay, exit_event)
            index_bulk(db, bulk, exit_event, pile_dir, retry)
        else:
            log.error(e)
            if type(e) == helpers.errors.BulkIndexError:
                backup_file_prefix = "crashed_index_bulk"
                log.error("WARNING: Could not index bulk of {} tweets after {} retries, giving up and backing up {} file in {}".format(len(bulk), MAX_RETRIES, backup_file_prefix, pile_dir))
                write_pile(None, bulk, os.path.join(pile_dir, backup_file_prefix))
            else:
                log.error("DEPILER CAN'T CONNECT TO ELASTICSEARCH. ENDING COLLECTION.")
                exit_event.set()


def depiler(pile, pile_deleted, pile_catchup, pile_media, conf, locale, exit_event):
    db = ElasticManager(**conf['database'])
    todo = []
    pile_dir = os.path.join(conf["path"], "piles")
    load_pile(pile_dir, "pile_main", pile)
    load_pile(pile_dir, "pile_deleted", pile_deleted)
    while not exit_event.is_set():
        pilesize = pile.qsize()
        if pilesize:
            log.info("Pile length: " + str(pilesize))
        try:
            while not pile_deleted.safe_empty():
                todelete = pile_deleted.get()
                db.set_deleted(todelete)
            todo = []
            while pilesize and len(todo) < DEPILER_BATCH_SIZE:
                todo.append(pile.get())
                pilesize -= 1
            if todo:
                log.debug("Preparing to index {} collected tweets".format(len(todo)))
            tweets_bulk = []
            for t in prepare_tweets(todo, locale):
                if db.multi_index and db.nb_past_months:
                    tweet_date = datetime.strptime(t["local_time"], FORMATTED_TWEET_DATETIME_FORMAT)
                    if db.is_too_old(tweet_date):
                        log.debug("Tweet {} is older than {} month{} and will not be saved.".format(
                            t["id"], db.nb_past_months, "s" if db.nb_past_months > 1 else ""
                        ))
                        continue
                if pile_media and t["media_files"]:
                    pile_media.put(t)
                if pile_catchup and t["to_tweetid"]:
                    if not db.find_tweet(t["to_tweetid"]):
                        pile_catchup.put(t["to_tweetid"])
                tweets_bulk.append(t)
            if tweets_bulk:
                index_bulk(db, tweets_bulk, exit_event, pile_dir)
        except Exception as e:
            log.error(str(type(e)) + ": " + str(e))
            log.error("ENDING COLLECTION.")
            exit_event.set()
            break
        breakable_sleep(2, exit_event)
    #TODO: move write_pile openation to main process, after all other processes are dead
    write_pile(pile_deleted, [], os.path.join(pile_dir, "pile_deleted"))
    write_pile(pile, todo, os.path.join(pile_dir, "pile_main"))
    log.info("FINISHED depiler")


def download_media(tweet, media_id, media_url, media_dir="media"):
    subdir = os.path.join(media_dir, media_id.split('_')[0][:-15])
    created_dir = False
    if not os.path.exists(subdir):
        os.makedirs(subdir)
        created_dir = True
    filepath = os.path.join(subdir, media_id)
    if os.path.exists(filepath):
        return 0
    try:
        r = requests.get(media_url, stream=True)
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return 1
    except Exception as e:
        log.warning("Could not download media %s for tweet %s (%s: %s)" % (media_url, tweet["url"], type(e), e))
        if created_dir:
            os.rmdir(subdir)
        return 0


def downloader(pile_media, media_dir, media_types, exit_event):
    while not exit_event.is_set() or not pile_media.safe_empty():
        todo = []
        while not pile_media.safe_empty():
            todo.append(pile_media.get())
        if not todo:
            breakable_sleep(2, exit_event)
            continue
        done = 0
        for tweet in todo:
            for enum, media_id in enumerate(tweet["media_files"]):
                if tweet["media_types"][enum] in media_types:
                    done += download_media(tweet, media_id, tweet["media_urls"][enum], media_dir)
        if done:
            log.debug("+%s files" % done)
    log.info("FINISHED downloader")

# TODO
# - mark as deleted tweet_ids missing from request result
def catchupper(pile, pile_catchup, oauth, oauth2, exit_event, conf):
    twitterco, _, _ = instantiate_clients(oauth, oauth2)
    pile_dir = os.path.join(conf["path"], "piles")
    load_pile(pile_dir, "pile_catchup", pile_catchup)
    todo = []
    while not exit_event.is_set():
        while not pile_catchup.safe_empty() and len(todo) < 100:
            todo.append(pile_catchup.get())
        if todo and not exit_event.is_set():
            try:
                tweets = twitterco.statuses.lookup(_id=",".join(todo), tweet_mode="extended", _method="POST")
            except (TwitterError, TwitterHTTPError, BadStatusLine, URLError, SSLError) as e:
                log.warning("API connection could not be established, retrying in 10 secs (%s: %s)" % (type(e), e))
                for t in todo:
                    pile_catchup.put(t)
                breakable_sleep(10, exit_event)
                continue
            if tweets and not exit_event.is_set():
                log.debug("+%d tweets" % len(tweets))
                for t in tweets:
                    t["collection_source"] = "thread"
                    pile.put(dict(t))
            todo = []
        breakable_sleep(5, exit_event)
    time.sleep(5)
    write_pile(pile_catchup, todo, os.path.join(pile_dir, "pile_catchup"))
    log.info("FINISHED catchupper")


def resolver(batch_size, db_conf, exit_event, verbose=False, url_debug=False, resolving_delay=30):
    db = prepare_db(**db_conf)
    skip = 0
    done = 0
    while not exit_event.is_set():
        try:
            todo = count_and_log(db, batch_size, done=done, skip=skip, retry_days=resolving_delay)
            done, skip = resolve_loop(batch_size, db, todo, skip, verbose=verbose, url_debug=url_debug,
                                  retry_days=resolving_delay)
        except exceptions.ConnectionError as e:
            log.error(e)
            log.error("RESOLVER CAN'T CONNECT TO ELASTICSEARCH. ENDING URLS RESOLUTION.")
            exit_event.set()
            break
        breakable_sleep(30, exit_event)
    log.info("FINISHED resolver")

real_min = lambda x, y: min(x, y) if x else y
date_to_time = lambda x: time.mktime(datetime.strptime(x[:16], "%Y-%m-%d %H:%M").timetuple())
re_andor = re.compile(r'(\([^)]+( OR [^)]+)*\) ?)+$')
re_ands = re.compile(r'\s+(AND|\+)\s+')
clean_ands = lambda x: re_ands.sub(" ", x).strip()
re_rich_query = re.compile(r"[*:]| OR ")

def format_keyword(k):
    k = k.strip()
    if k.startswith('@'):
        k = k.lstrip('@')
        return "from:%s OR to:%s OR @%s" % (k, k, k)
    if " AND " in k or " + " in k:
        k = "(%s)" % clean_ands(k)
    return quote(k.encode('utf-8'), ' ()*:')

def format_url_queries(urlpieces):
    return [format_url_query(q) for q in urlpieces]

re_split_url_pieces = re.compile(r'[^a-z0-9]+', re.I)
def format_url_query(urlquery):
    return " ".join([k for k in re_split_url_pieces.split(urlquery) if k.strip()])

def streamer(pile, pile_deleted, oauth, oauth2, conf, locale, language, geocode, exit_event):
    keywords = conf["keywords"]
    urlpieces = conf["url_pieces"]
    timed_keywords = conf["time_limited_keywords"]

    resco, _, streamco = instantiate_clients(oauth, oauth2)

    # Stream parameters reference: https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters
    # Stream operators reference: https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators.html
    # Stream special messages reference: https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/streaming-message-types
    while not exit_event.is_set():
        ts = time.time()
        extra_keywords = []

        # handle timed keywords and find first date when to stop
        end_time = None
        for keyw, planning in timed_keywords.items():
            for times in planning:
                t0 = date_to_time(times[0])
                t1 = date_to_time(times[1])
                if t0 < ts < t1:
                    extra_keywords.append(keyw)
                    end_time = real_min(end_time, t1)
                    break
                elif t0 > ts:
                    end_time = real_min(end_time, t0)
        log.info('Starting stream track until %s' % end_time)

        try:
            # keywords tracked on stream
            query_keywords = [clean_ands(k).lower() for k in keywords + format_url_queries(urlpieces) + extra_keywords if not re_rich_query.search(k) and not k.startswith('@')]
            filter_keywords = [clean_ands(k).lower() for k in keywords + urlpieces + extra_keywords if not re_rich_query.search(k) and not k.startswith('@')]
            for k in keywords + extra_keywords:
                if re_rich_query.search(k):
                    if re_andor.match(k) and "*" not in k and ":" not in k:
                        ands = [o.split(' OR ') for o in k.strip('()').split(') (')]
                        combis = ands[0]
                        for ors in ands[1:]:
                            combis = ["%s %s" % (a, b) for a in combis for b in ors]
                        query_keywords += combis
                        filter_keywords += combis
                    else:
                        log.warning('Ignoring keyword %s to streaming API, please use syntax with simple queries (no * wildcards nor filter: url: or else) separated by spaces or such as "(KEYW1 OR KEYW2) (KEYW3 OR KEYW4 OR KEYW5) (KEYW6)"' % k)

            # users followed on stream
            users = [k.lstrip('@').strip().lower() for k in keywords + extra_keywords if k.startswith('@')]
            keep_users = list(users)
            query_users = []
            while users:
                for u in resco.users.lookup(screen_name=','.join(users[0:100]), include_entities=False):
                    query_users.append(u['id_str'])
                users = users[100:]

            # prepare stream query arguments
            args = {'filter_level': 'none', 'stall_warnings': 'true'}
            if language:
                args['language'] = language
            if geocode:
                args['locations'] = geocode
            else:
                if query_keywords:
                    args['track'] = ",".join(query_keywords)
                if query_users:
                    args['follow'] = ",".join(query_users)

            streamiter = []
            if not (geocode or query_keywords or query_users):
                log.warning("No keyword is compatible with the stream API, only search API will be used.")
                while not exit_event.is_set():
                    breakable_sleep(86400, exit_event)
            else:
                log.debug("Calling stream with args %s" % args)
                streamiter = streamco.statuses.filter(**args)
        except KeyboardInterrupt:
            log.info("closing streamer...")
            exit_event.set()
        except (TwitterHTTPError, BadStatusLine, URLError, SSLError) as e:
            log.warning("Stream connection could not be established, retrying in 2 secs (%s: %s)" % (type(e), e))
            breakable_sleep(2, exit_event)
            continue

        try:
            for msg in streamiter:
                if exit_event.is_set():
                    break
                if end_time and end_time < time.time():
                    log.info("Reached time to update list of keywords")
                    break
                if not msg:
                    continue
                if msg.get("disconnect") or msg.get("hangup"):
                    log.warning("Stream connection lost: %s" % msg)
                    break
                if msg.get("timeout"):
                    continue
                if msg.get('id_str'):
                    msg["collection_source"] = "stream"
                    try:
                        for tweet in normalize_tweet(msg, locale=locale, extract_referenced_tweets=True):
                            if geocode or (urlpieces and not keywords):
                                tmptext = tweet["text"].lower()
                                keep = False
                                for k in filter_keywords:
                                    if " " in k:
                                        keep2 = True
                                        for k2 in k.split(" "):
                                            if k2 not in tmptext:
                                                keep2 = False
                                                break
                                        if keep2:
                                            keep = True
                                            break
                                    elif k in tmptext:
                                        keep = True
                                        break
                                if not keep and keep_users:
                                    tmpauthor = tweet['user_screen_name'].lower()
                                    for u in keep_users:
                                        if "@%s" % u in tmptext or u == tmpauthor:
                                            keep = True
                                            break
                                if not keep:
                                    continue
                            pile.put(preprocess_tweet_for_indexing(tweet))
                            log.debug("+1 tweet")
                    except KeyError as missing_field:
                        log.warning("Missing '{}' field in tweet: \n{}".format(missing_field, msg))
                        continue
                else:
                    if 'delete' in msg and 'status' in msg['delete'] and 'id_str' in msg['delete']['status']:
                        pile_deleted.put(msg['delete']['status']['id_str'])
                        log.debug("-1 tweet (deleted by user)")
                    else:
                        log.info("Got special data: %s" % str(msg))
        except (TwitterHTTPError, BadStatusLine, URLError, SSLError, socket.error) as e:
            log.warning("Stream connection lost, reconnecting in a sec... (%s: %s)" % (type(e), e))
        except KeyboardInterrupt as e:
            log.info("closing streamer (%s: %s)..." % (type(e), e))
            exit_event.set()
        except Exception as e:
            import traceback
            log.info("streamer crashed (%s: %s)..." % (type(e), e))
            log.error(traceback.format_exc())
            exit_event.set()

        if streamiter != []:
            log.debug("Stream stayed alive for %sh" % str(old_div((time.time()-ts),3600)))
            breakable_sleep(2, exit_event)
    log.info("FINISHED streamer")

chunkize = lambda a, n: [a[i:i+n] for i in range(0, len(a), n)]

def get_twitter_rates(conn, conn2, retry=0):
    try:
        rate_limits = conn.application.rate_limit_status(resources="search")['resources']['search']['/search/tweets']
        rate_limits2 = conn2.application.rate_limit_status(resources="search")['resources']['search']['/search/tweets']
    except URLError as e:
        if retry:
            time.sleep(1)
            return get_twitter_rates(conn, conn2, retry=retry-1)
        raise e
    return min(int(rate_limits['reset']), int(rate_limits2['reset'])), (rate_limits['limit'] + rate_limits2['limit']), (rate_limits['remaining'] + rate_limits2['remaining'])

def stall_queries(next_reset, exit_event):
    delay = max(1, int(next_reset - time.time())) + 1
    if delay > 5:
        log.info("Stalling search queries with rate exceeded for the next %s seconds" % delay)
    breakable_sleep(delay, exit_event)

def read_search_state(dir_path="."):
    state_file = os.path.join(dir_path, ".search_state.json")
    with open(state_file) as f:
        return {k: v for k, v in json.load(f).items()}

def write_search_state(state, dir_path="."):
    state_file = os.path.join(dir_path, ".search_state.json")
    with open(state_file, "w") as f:
        json.dump(state, f)

# TODO
# - improve logs : add INFO on result of all queries on a keyword if new

def searcher(pile, oauth, oauth2, conf, locale, language, geocode, exit_event, no_rollback=False, max_tweet_id=0):
    keywords = conf["keywords"]
    urlpieces = conf["url_pieces"]
    timed_keywords = conf["time_limited_keywords"]

    searchco, searchco2, _ = instantiate_clients(oauth, oauth2)

    # Search operators reference: https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
    try:
        next_reset, max_per_reset, left = get_twitter_rates(searchco, searchco2, retry=3)
    except Exception as e:
        log.error("Connecting to Twitter API: could not get rate limits %s: %s" % (type(e), e))
        sys.exit(1)
    curco = searchco

    queries = []
    fmtkeywords = []
    for k in keywords:
        if k.startswith("@"):
            queries.append(format_keyword(k))
        else:
            fmtkeywords.append(format_keyword(k))
    for q in urlpieces:
        fmtkeywords.append('url:"%s"' % format_url_query(q))
    if len(fmtkeywords) > 50:
        queries += ["(" + ") OR (".join(a) + ")" for a in chunkize(fmtkeywords, 3)]
    else:
        queries += fmtkeywords
    timed_queries = {}
    state = {q: 0 for q in queries + [format_keyword(k) for k in timed_keywords.keys()]}
    queries_since_id = {}
    try:
        queries_since_id = read_search_state(dir_path=conf["path"])
        assert queries_since_id and sorted(state.keys()) == sorted(queries_since_id.keys())
        log.info("Search queries restarting from previous state.")
    except Exception as e:
        for key in queries_since_id:
            if key in state and queries_since_id[key]:
                state[key] = queries_since_id[key]
        queries_since_id = state

    timegap = 1 + len(queries)
    while not exit_event.is_set():
      try:
        if time.time() > next_reset:
            try:
                next_reset, _, left = get_twitter_rates(searchco, searchco2, retry=1)
            except Exception as e:
                log.error("Issue while collecting twitter rates, applying default 15 min values. %s: %s" % (type(e), e))
                next_reset += 15*60
                left = max_per_reset
        if not left:
            stall_queries(next_reset, exit_event)
            continue

        log.info("Starting search queries cycle with %d remaining calls for the next %s seconds" % (left, int(next_reset - time.time())))

        now = time.time()
        last_week = now - 60*60*24*7
        for keyw, planning in timed_keywords.items():
            keyw = format_keyword(keyw)
            timed_queries[keyw] = []
            for times in planning:
                t0 = date_to_time(times[0])
                t1 = date_to_time(times[1])
                if last_week < t0 < now or last_week < t1 < now:
                    timed_queries[keyw].append([t0, t1])

        for query in [q[0] for q in sorted(queries_since_id.items(), key=lambda ts: ts[1])]:
            try:
                planning = timed_queries[query]
                if not planning:
                    continue
            except KeyError:
                planning = None

            since = queries_since_id[query]
            max_id = max_tweet_id
            log.debug("Starting search query on %s since %s" % (query, since))
            while not exit_event.is_set():
                while not left and not exit_event.is_set():
                    try:
                        next_reset, _, left = get_twitter_rates(searchco, searchco2, retry=1)
                        if left:
                            log.debug("Resuming search with %d remaining calls for the next %s seconds" % (left, int(next_reset - time.time())))
                        else:
                            log.debug("No more queries available, stalling until %s" % next_reset)
                    except Exception as e:
                        log.debug("Issue while collecting twitter rates. %s: %s" % (type(e), e))
                    if not left:
                        stall_queries(next_reset, exit_event)

                args = {'q': query, 'count': 100, 'include_entities': True, 'result_type': 'recent', 'tweet_mode': 'extended'}
                if language:
                    args['lang'] = language
                if geocode:
                    args['geocode'] = geocode
                if max_id:
                    args['max_id'] = str(max_id)
                if queries_since_id[query]:
                    args['since_id'] = str(queries_since_id[query])
                try:
                    res = curco.search.tweets(**args)
                except (TwitterError, TwitterHTTPError, BadStatusLine, URLError, SSLError) as e:
                    curco = searchco if curco == searchco2 else searchco2
                    log.info("Switching search connexion to OAuth%s" % (2 if curco == searchco2 else ""))
                    try:
                        res = curco.search.tweets(**args)
                    except (TwitterError, TwitterHTTPError, BadStatusLine, URLError, SSLError) as e:
                        log.warning("Search connection could not be established, retrying in 2 secs (%s: %s)" % (type(e), e))
                        breakable_sleep(2, exit_event)
                        continue
                left -= 1
                try:
                    tweets = res['statuses']
                except KeyError:
                    log.warning("Bad response from Twitter to query %s with args %s: %s" % (query, args, res))
                    breakable_sleep(2, exit_event)
                    continue
                if not len(tweets):
                    if not exit_event.is_set():
                        queries_since_id[query] = since
                        write_search_state(queries_since_id, dir_path=conf["path"])
                    break
                news = 0
                for tw in tweets:
                    tid = int(tw.get('id_str', str(tw.get('id', ''))))
                    if not tid:
                        continue
                    if since < tid:
                        since = tid + 1
                        if no_rollback and not queries_since_id[query]:
                            break
                    if not max_id or max_id > tid:
                        max_id = tid - 1
                    if planning is not None:
                        ts = get_timestamp(tw["created_at"])
                        skip = True
                        for trang in planning:
                            if trang[0] < ts < trang[1]:
                                skip = False
                                break
                        if skip:
                            continue
                    tw["collection_source"] = "search"
                    pile.put(dict(tw))
                    news += 1
                if news:
                    log.debug("+%d tweets (%s since %s until %s)" % (news, query, queries_since_id[query], max_id))
                else:
                    if not exit_event.is_set():
                        queries_since_id[query] = since
                        write_search_state(queries_since_id, dir_path=conf["path"])
                    break

        breakable_sleep(max(timegap, next_reset - time.time() - 1.5*left), exit_event)
      #TODO: indent 4 spaces
      except KeyboardInterrupt:
        log.info( "closing searcher...")
        exit_event.set()
    log.info("FINISHED searcher")

def generate_geoloc_strings(x1, y1, x2, y2):
    streamgeocode = "%s,%s,%s,%s" % (y1, x1, y2, x2)
    log.info('Stream Bounding box: %s/%s -> %s/%s' % (x1, y1, x2, y2))
    x = old_div((x1 + x2), 2)
    y = old_div((y1 + y2), 2)
    d = 6371 * acos(sin(x*pi/180) * sin(x1*pi/180) + cos(x*pi/180) * cos(x1*pi/180) * cos((y1-y)*pi/180))
    searchgeocode = "%s,%s,%.2fkm" % (x, y, d)
    log.info('Search Disk: %s/%s, %.2fkm' % (x, y, d))
    return streamgeocode, searchgeocode


def main(conf, path=".", max_id=0):
    if len(conf['keywords']) + len(conf['url_pieces']) > 400:
        log.error('Please limit yourself to a maximum of 400 keywords total (including url_pieces): you set up %s keywords and %s url_pieces.' % (len(conf['keywords']), len(conf['url_pieces'])))
        sys.exit(1)
    try:
        oauth, oauth2 = get_oauth(conf)
    except Exception as e:
        log.error('Could not initiate connections to Twitter API: %s %s' % (type(e), e))
        sys.exit(1)

    try:
        locale = timezone(conf['timezone'])
    except Exception as e:
        log.error("\t".join(all_timezones)+"\n\n")
        log.error('Unknown timezone set in config.json: %s. Please choose one among the above ones.' % conf['timezone'])
        sys.exit(1)
    try:
        db = ElasticManager(**conf['database'])
        db.prepare_indices()
    except Exception as e:
        log.error('Could not initiate connection to database: %s %s' % (type(e), e))
        sys.exit(1)
    language = conf.get('language', None)
    streamgeocode = None
    searchgeocode = None
    if "geolocation" in conf and conf["geolocation"]:
        if type(conf["geolocation"]) == list:
            try:
                x1, y1, x2, y2 = conf["geolocation"]
                streamgeocode, searchgeocode = generate_geoloc_strings(x1, y1, x2, y2)
            except Exception as e:
                log.error('geolocation is wrongly formatted, should be something such as ["Lat1", "Long1", "Lat2", "Long2"]')
                sys.exit(1)
        else:
            geoconn, _, _ = instantiate_clients(oauth, oauth2)
            res = geoconn.geo.search(query=conf["geolocation"].replace(" ", "+"), granularity=conf.get("geolocation_type", "admin"), max_results=1)
            try:
                place = res["result"]["places"][0]
                log.info('Limiting tweets search to place "%s" with id "%s"' % (place['full_name'], place['id']))
                y1, x1 = place["bounding_box"]['coordinates'][0][0]
                y2, x2 = place["bounding_box"]['coordinates'][0][2]
                streamgeocode, searchgeocode = generate_geoloc_strings(x1, y1, x2, y2)
            except Exception as e:
                log.error('Could not find a place matching geolocation %s: %s %s' % (conf["geolocation"], type(e), e))
                sys.exit(1)
    grab_conversations = "grab_conversations" in conf and conf["grab_conversations"]
    resolve_links = "resolve_redirected_links" in conf and conf["resolve_redirected_links"]
    resolving_delay = int(conf["resolving_delay"]) if "resolving_delay" in conf else 30
    no_rollback = "catchup_past_week" not in conf or not conf["catchup_past_week"]
    if "download_media" in conf and conf["download_media"]:
        try:
            media_dir = conf["download_media"].pop("media_directory")
        except KeyError:
            media_dir = "media"
        dl_media = any(conf["download_media"].values())
    else:
        dl_media = False
    if dl_media:
        media_types = set([k for k in conf["download_media"] if conf["download_media"][k]])
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)
    pile = Queue()
    pile_deleted = Queue()
    pile_catchup = Queue() if grab_conversations else None
    pile_media = Queue() if dl_media else None
    default_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    exit_event = Event()
    depile = Process(
        target=depiler,
        args=(pile, pile_deleted, pile_catchup, pile_media, conf, locale, exit_event),
        daemon=True,
        name="depiler   "
    )
    start_process(depile, path)
    if grab_conversations:
        catchup = Process(
            target=catchupper,
            args=(pile, pile_catchup, oauth, oauth2, exit_event, conf),
            daemon=True,
            name="catchupper"
        )
        start_process(catchup, path)
    if resolve_links:
        resolve = Process(
            target=resolver,
            args=(RESOLVER_BATCH_SIZE, conf['database'], exit_event, resolving_delay),
            daemon=True,
            name="resolver  "
        )
        start_process(resolve, path)
    if dl_media:
        download = Process(
            target=downloader,
            args=(pile_media, media_dir, media_types, exit_event),
            daemon=True,
            name="downloader"
        )
        start_process(download, path)
    signal.signal(signal.SIGINT, default_handler)
    if conf["start_stream"]:
        stream = Process(
            target=streamer,
            args=(pile, pile_deleted, oauth, oauth2, conf, locale, language, streamgeocode, exit_event),
            daemon=True,
            name="streamer  "
        )
        start_process(stream, path)
    search = Process(
        target=searcher,
        args=(pile, oauth, oauth2, conf, locale, language, searchgeocode, exit_event, no_rollback, max_id),
        daemon=True,
        name="searcher  "
    )
    start_process(search, path)

    def stopper(*args):
        exit_event.set()

    signal.signal(signal.SIGTERM, stopper)

    try:
        depile.join()
    except KeyboardInterrupt:
        stopped = stop(path)
        if stopped:
            log.info("Collection stopped.")
            unresolved_urls = db.count_tweets("links_to_resolve", True)
            if unresolved_urls:
                log.info("{} tweets contain unresolved urls. Run 'gazou resolve' if you want to resolve all urls."
                    .format(unresolved_urls)
                         )


if __name__=='__main__':
    main(load_conf("."), ".")
