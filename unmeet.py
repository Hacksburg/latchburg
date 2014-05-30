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
      print "can't open ACL file (/var/lib/latchburg/db.acl): JSON Decode error"
      return 1;
    except IOError:
      print "can't open ACL file (/var/lib/latchburg/db.acl): IO error"
      return 1;

    print "Users:"
    for user in data.values().sort():
        print user

    print

    username = raw_input('Username to delete: ')

    for key, val in data.items():
        if val == username:
            print "removing user " + username + ", with key hash "
            print key
            data.pop(key)

    with open('/var/lib/latchburg/db.acl', 'w') as f:
      f.write(simplejson.dumps(data))


if __name__ == "__main__":
  exit(main())

