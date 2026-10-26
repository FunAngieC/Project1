# # import serial, time, re, sqlite3

# # ser = serial.Serial("/dev/cu.usbmodemE8F60AD4CA7C2", 115200, timeout=2)
# # time.sleep(2)              # some boards reset when the port opens
# # ser.reset_input_buffer()   # drop anything stale
# # ser.readline()             # discard the first, possibly partial, line

# # pattern = re.compile(r"IR=(\d+), BPM=([\d.]+), Avg BPM=(\d+)")


# # def update_database(data):
# #     #accesses database.db
# #     con = sqlite3.connect("database.db")
# #     cur = con.cursor()
# #     #creates heartrate table with time, IR, BPM, and avg bpm if it does not already exist
# #     cur.execute("CREATE TABLE IF NOT EXISTS heartrate(time, IR, BPM, avg_bpm)")
# #     #adds the data into the table
# #     cur.executemany("INSERT INTO heartrate VALUES(?, ?, ?, ?)", data)
# #     con.commit()
# #     #!!!!What does this do?
# #     res = cur.execute('SELECT * FROM "heartrate"')
# #     output = res.fetchone()
# #     print(output)
# #     con.close()

# # while True:
# #     line = ser.readline().decode("utf-8", errors="ignore").strip()
# #     m = pattern.search(line)
# #     if not m:
# #         continue           # skip partial or garbled lines
# #     ir, bpm, avg = int(m[1]), float(m[2]), int(m[3])
# #     no_finger = "No finger" in line
# #     output = (time.time(), ir, bpm, avg, no_finger)

# #     update_database(output)



# import serial, time, re, sqlite3

# ser = serial.Serial("/dev/cu.usbmodemE8F60AD4CA7C2", 115200, timeout=2)
# time.sleep(2)              # some boards reset when the port opens
# ser.reset_input_buffer()   # drop anything stale
# ser.readline()             # discard the first, possibly partial, line

# pattern = re.compile(r"IR=(\d+), BPM=([\d.]+), Avg BPM=(\d+)")

# # open the database once, before the loop
# con = sqlite3.connect("real_database.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS heartrate(time REAL, IR INTEGER, BPM REAL, avg_bpm INTEGER)")
# con.commit()


# def update_database(row):
#     cur.execute("INSERT INTO heartrate VALUES(?, ?, ?, ?)", row)
#     con.commit()


# while True:
#     line = ser.readline().decode("utf-8", errors="ignore").strip()
#     print("RAW:", repr(line), flush=True)
#     m = pattern.search(line)
#     if not m:
#         continue                # skip partial or garbled lines


#     ir, bpm, avg = int(m[1]), float(m[2]), int(m[3])

#     if "No finger" in line or ir < 50000 or bpm < 40 or bpm > 180:
#         continue                 # skip readings with no finger on the sensor

#     row = (time.time(), ir, bpm, avg)
#     update_database(row)
#     print(row)

# # import serial, time, re, sqlite3

# # ser = serial.Serial("/dev/cu.usbmodemE8F60AD4CA7C2", 115200, timeout=2)
# # time.sleep(2)              # some boards reset when the port opens
# # ser.reset_input_buffer()   # drop anything stale
# # ser.readline()             # discard the first, possibly partial, line

# # pattern = re.compile(r"IR=(\d+), BPM=([\d.]+), Avg BPM=(\d+)")


# # def update_database(data):
# #     #accesses database.db
# #     con = sqlite3.connect("database.db")
# #     cur = con.cursor()
# #     #creates heartrate table with time, IR, BPM, and avg bpm if it does not already exist
# #     cur.execute("CREATE TABLE IF NOT EXISTS heartrate(time, IR, BPM, avg_bpm)")
# #     #adds the data into the table
# #     cur.executemany("INSERT INTO heartrate VALUES(?, ?, ?, ?)", data)
# #     con.commit()
# #     #!!!!What does this do?
# #     res = cur.execute('SELECT * FROM "heartrate"')
# #     output = res.fetchone()
# #     print(output)
# #     con.close()

# # while True:
# #     line = ser.readline().decode("utf-8", errors="ignore").strip()
# #     m = pattern.search(line)
# #     if not m:
# #         continue           # skip partial or garbled lines
# #     ir, bpm, avg = int(m[1]), float(m[2]), int(m[3])
# #     no_finger = "No finger" in line
# #     output = (time.time(), ir, bpm, avg, no_finger)

# #     update_database(output)



# import serial, time, re, sqlite3

# ser = serial.Serial("/dev/cu.usbmodemE8F60AD4CA7C2", 115200, timeout=2)
# time.sleep(2)              # some boards reset when the port opens
# ser.reset_input_buffer()   # drop anything stale
# ser.readline()             # discard the first, possibly partial, line

# pattern = re.compile(r"IR=(\d+), BPM=([\d.]+), Avg BPM=(\d+)")

# # open the database once, before the loop
# con = sqlite3.connect("real_database.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS heartrate(time REAL, IR INTEGER, BPM REAL, avg_bpm INTEGER)")
# con.commit()


# def update_database(row):
#     cur.execute("INSERT INTO heartrate VALUES(?, ?, ?, ?)", row)
#     con.commit()


# while True:
#     line = ser.readline().decode("utf-8", errors="ignore").strip()
#     print("RAW:", repr(line), flush=True)
#     m = pattern.search(line)
#     if not m:
#         continue                # skip partial or garbled lines


#     ir, bpm, avg = int(m[1]), float(m[2]), int(m[3])

#     if "No finger" in line or ir < 50000 or bpm < 40 or bpm > 180:
#         continue                 # skip readings with no finger on the sensor

#     row = (time.time(), ir, bpm, avg)
#     update_database(row)
#     print(row)


import serial, time, re, sqlite3, pandas
 
PORT = "/dev/cu.usbmodemE8F60AD4CA7C2"
BAUD = 115200
 
pattern = re.compile(r"IR=(\d+), BPM=([\d.]+), Avg BPM=(\d+)")
 
con = sqlite3.connect("real_database.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS heartrate(time REAL, IR INTEGER, BPM REAL, avg_bpm INTEGER)")
con.commit()
 
 
def update_database(row):
    cur.execute("INSERT INTO heartrate VALUES(?, ?, ?, ?)", row)
    con.commit()
 
 
def open_port():
    # keep trying until the board is available
    while True:
        try:
            s = serial.Serial(PORT, BAUD, timeout=2)
            try:
                s.dtr = False        # toggle DTR so the board sees a fresh connection
                time.sleep(0.1)
                s.dtr = True
            except OSError:
                pass                 # some ports don't support this; carry on
            s.reset_input_buffer()
            print("Connected to", PORT, flush=True)
            return s
        except serial.SerialException as e:
            print("Can't open port, retrying in 2 s:", e, flush=True)
            time.sleep(2)
 
 
ser = open_port()
empty_count = 0
last_saved = 0                       # time of the last saved reading
 
try:
    while True:
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
        except serial.SerialException:
            print("Lost connection, reconnecting...", flush=True)
            ser.close()
            ser = open_port()
            continue
 
        if not line:
            empty_count += 1
            if empty_count >= 3:     # about 6 seconds of silence
                print("No data, reconnecting...", flush=True)
                ser.close()
                ser = open_port()
                empty_count = 0
            continue
        empty_count = 0
 
        m = pattern.search(line)
        if not m:
            continue                 # skip partial or garbled lines
 
        ir, bpm, avg = int(m[1]), float(m[2]), int(m[3])
 
        if "No finger" in line or ir < 50000 or bpm < 40 or bpm > 180:
            continue                 # skip no-finger readings and impossible heart rates
 
        time_value = time.time()
        now = pandas.to_datetime(time_value, unit="s")     
        if time_value - last_saved < 0.5:
            continue                 # already saved a reading this second
        last_saved = time_value
 
        row = (str(now), ir, bpm, avg)
        update_database(row)
        print("SAVED:", row, flush=True)
except KeyboardInterrupt:
    print("Stopping...")
finally:
    ser.close()                      # release the port so the next run (or the Arduino IDE) can use it
    con.close()
 