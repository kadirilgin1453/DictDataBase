import dictdatabase as DDB
from pyinstrument import profiler


def a_create():
	d = {"key1": "val1", "key2": 2, "key3": [1, "2", [3, 3]]}
	for i in range(4):
		d = {f"key{i}{j}": d for j in range(20)}
	# About 22MB
	DDB.at("_test_big_db").create(d, force_overwrite=True)


def b_read():
	d = DDB.at("_test_big_db").read()


def c_session():
	with DDB.at("_test_big_db").session() as (session, d):
		session.write()





p = profiler.Profiler(interval=0.00001)
p.start()

for f in [a_create, b_read, c_session]:
	for _ in [False, True]:
		for _ in [False, True]:
			for _ in [False, True]:
				for _ in [None, 0, 2, "\t"]:
					# TODO: missing configs
					f()

p.stop()

p.open_in_browser(timeline=True)
