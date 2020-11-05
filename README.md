# srml
**Author: Jeefy**  
**Email: jeefy163@163.com**  
**Url: [Github](https://github.com/jeefies/srml), [PyPI](https://pypi.org/project.srml)**

-----------
## Connections

### SMTPConnect
A easy smtp connect class to connect smtp host.   
Initialize with four params:  
host: refers to the connect host, such as 'smtp.qq.com'.  
mails: refers to the user's info, format in ('email@some.com', 'password').  
> Notice:  
> The password is the password for login the smtp, imap, pop hosts.  
ssl: decide whether use ssl to connect or not.  
port: the connect port of the host.  

- login  
    `login(email, passwd)`, if param email or passwd if not given, use the info recieve when create the instance.  
- send  
    `send(msg)`, bind with Message class.  
- close  
    `close()`, disconnect with the host and quit.  
> Can use `with SMTPConnect(...) as conn`.  
> If `with` is used, this would automatic use `.login` method.  

### IMAPConnect
Almost the same as SMTPConnect.
- login  
    `login(email, passwd)`, the same as SMTPConnect.  
- select_folder  
    `select_folder('Folder name')`, select folder accordng to `list_folders()`  
- list_folders  
    `list_folders()`, return all exists folders can be select.  
- close_folder  
    `close_folder()`, close the current select folder.  
    > if need to unselect, use `.client.unselect_folder()`
- search  
    `search(types=['ALL'])`, search the emails according to the types, default 'ALL'  
- fetch  
    `fetch(uid, types='BODY[]')`, fetch the message according to the search returned uids.  
- fetchall  
    `fetchall(types='BODY[]')`, return all message.  
- quit  
    exit the connection.  

### POPConnect
See also srml.popclient.POPClient.
Like poplib.POP or poplib.POP_SSL.
more infomation, see [python standard library](https://docs.python.org/3/library/poplib.html)

-------------------
## Parse
Parse the MIME message according to the bytes in.  
shown body see `Parse.body`.  
plain text see `Parse.text`.  
params or files see `Parse.get_params()`.  
more see `Parse.dict`  

### File
A class help to save the file.

---------------------------------
## MailBox
**The mix class for all connection**  
use `help(MailBox)` for more details.  

------------------
## srml.mailG
the GUI version to use the email objects.  
## srml.mailCli
The cli version to use the email objects.  