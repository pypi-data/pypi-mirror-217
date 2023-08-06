## **Onion-Server - Dot-Onion and hidden services manager and client**

---

Onion-Server provides a client for fast and easy Hidden services management. Helps in controlling services in one session.
<br>

### **Installation**

```bash
sudo su
python -m pip install onion-server
```

<br>

### **OS Support**

- Linux

---

<br>

## **Usage**

### **server**

```bash
$ server.<command>
```

**start** - start server  
**stop** - stop server  
**scan** - scan server for unrecorded changes  
**reboot** | restart - restart or reboot server

<br>

### **tor**

```bash
$ tor.<command>
```

**start** - start tor service  
**stop** - stop tor service

<br>

### **http**

```bash
$ http.<command>
```

**start** - start http service  
**stop** - stop http service

<br>

### **web**

```bash
$ web.<command>
```

**info** - display web services status  
**dir** [ path ] - set new web files dir

```bash
$ web.dir <path>
```

**set** [ status ] - set web status

```bash
$ web.set <command>
```

**online** - set web service online  
**offline** - set web service offline

<br>

### **Others**

```bash
$ <command>
```

**reset** - reset server  
**scan** - update all running services on the server  
**status** - display server services status  
**exit** - quit server
