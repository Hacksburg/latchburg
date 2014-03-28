import doorman.attempts
import hashlib
import simplejson

from lockfile import FileLock

def main():
  with FileLock('/var/lib/latchburg/db.acl'):
    try:
      with open('/var/lib/latchburg/db.acl', 'r') as f:
        data = simplejson.loads(f.read())
    except simplejson.scanner.JSONDecodeError:
      data = {}
    except IOError:
      data = {}

    username = raw_input('Username: ')

    print "Swipe Card Twice."
    attempt = doorman.attempts.EntryAttemptInterface().getAttempt()

    hasher = hashlib.sha512()
    hasher.update(attempt)
    data[hasher.hexdigest()] = username

    with open('/var/lib/latchburg/db.acl', 'w') as f:
      f.write(simplejson.dumps(data))


if __name__ == "__main__":
  main()

