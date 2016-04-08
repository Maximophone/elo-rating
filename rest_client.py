import httplib
import json

ADDRESS = 'localhost:5656'

conn = httplib.HTTPConnection(ADDRESS)
headers = {"Content-type": "application/json", "Accept": "text/plain"}
cmd = ["GET",'','']

while 1:
    try:
        conn.connect()
        conn.request(cmd[0],'/elo/api/v1.0/'+cmd[1],cmd[2],headers)
    except:
        print "Server cannot be reached at the moment. Retry? (y/n)"
        if raw_input().lower() in ('y','yes'):
            conn.close()
            continue
        exit(0)
    rsp = conn.getresponse()
    try: data = json.loads(rsp.read())
    except ValueError:
        print 'Invalid response from server. Retry? (y/n)'
        if raw_input().lower() in ('y','yes'): continue
        exit(0)
    if data.get('content'):
        print data['content'] + '\n'
    menu = data.get('menu')
    if menu:
        for i,menu_element in enumerate(menu):
            print "%d. %s"%(i+1,menu_element[0])
        print "0. Exit"
        while 1:
            try:
                choice = int(raw_input())
                if choice<=len(menu): break
                print "Invalid choice"
            except ValueError:
                print "Invalid input"
        if choice==0: exit(0)
        menu_element = menu[choice-1]
        method = menu_element[1]
        if method == "GET":
            cmd = [method,menu_element[2],'']
        elif method=="POST":
            values = {}
            for alias,var in menu_element[3]:
                values[var] = raw_input("%s: "%alias)
            cmd = [method,menu_element[2],json.dumps(values)]

conn.close()