import yaml
from jinja2 import Environment, FileSystemLoader
import os, os.path as osp
from pprint import pprint
from copy import deepcopy

# popular trackers
extra_trackers = '''
tr=wss%3A%2F%2Ftracker.btorrent.xyz
tr=wss%3A%2F%2Ftracker.fastcast.nz
'''

# webtorrent hosted trackers
extra_trackers += '''
tr=wss%3A%2F%2Ftracker.openwebtorrent.com
'''

# Lyken's self-hosted tracker (Japan) as backup
extra_trackers += '''
tr=http%3A%2F%2Ffrp-jp.lzhu.me%3A8000%2Fannounce
tr=udp%3A%2F%2Ffrp-jp.lzhu.me%3A8000
tr=ws%3A%2F%2Ffrp-jp.lzhu.me%3A8000
'''

# Lyken's self-hosted tracker (China) as backup
# extra_trackers += '''
# tr=http%3A%2F%2Fcn.tr.syu.life%3A8080%2Fannounce
# tr=udp%3A%2F%2Fcn.tr.syu.life%3A8080
# tr=ws%3A%2F%2Fcn.tr.syu.life%3A8080
# '''

extra_trackers = [_ for _ in extra_trackers.strip().split("\n") if len(_) > 2]

# extra_trackers = "&".join(extra_trackers)
# print(extra_trackers)

def load_yaml(filename):
	with open(filename, 'rb' ) as f:
		return yaml.load( f, Loader=yaml.FullLoader)

def generate_bangumi(curr_data, meta, prev_data=None, next_data=None, extra_trackers=extra_trackers, dirname="docs", ):
	env = Environment(
		loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))),
		trim_blocks=True
	)
	template = env.get_template('template_bangumi.html')
	'''
	data:
		magnetlink:
		torrent:
		name:
	'''
	# prev_id, curr_id, next_id = ("ep-%d.html" % (index + i) for i in (-1, 0, 1))
	curr_id = curr_data["episode"]
	
	temp_trackers = deepcopy(extra_trackers)
	# global meta
	if 'webseeds' in meta:
		episode = curr_data["episode"]
		webseeds = meta['webseeds']
		if 'lambda' in webseeds:
			episode = eval(webseeds['lambda'])
		# webseeds['torrent'].format(episode=episode)
		if 'torrent' in webseeds:
			temp_trackers.append("xs=%s" % webseeds['torrent'].format(episode=episode))
		if 'video' in webseeds:
			temp_trackers.append("ws=%s" % webseeds['video'].format(episode=episode))
	pprint(temp_trackers)
	# exit(0)
	htmlpage = template.render(
			prev=prev_data, 
			curr=curr_data, 
			next=next_data, 
			extra_trackers="&" + "&".join(temp_trackers),
			meta=meta,
		)
	
	# filename = "docs/ep-%s.html" % curr_id
	filename = osp.join(dirname, "ep-%s.html" % curr_id)
	with open(filename, 'w') as f:
		f.write(htmlpage)
		print("Successfuly generate_bangumi %s" % filename)

def generate_index(bangumi, dirname="docs"):
	env = Environment(
		loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))),
		trim_blocks=True
	)
	template = env.get_template('template_index.html')

	htmlpage = template.render(
			tumi=yinfo['tumi'],
			meta=yinfo['meta']
		)
	
	# filename = "docs/index.html"
	filename = osp.join(dirname, "index.html")
	with open(filename, 'w') as f:
		f.write(htmlpage)
		print("Successfuly generate_index %s" % filename)

bangumi = "Shingeki no Kyojin"	
# bangumi = "Kimetsu no Yaiba"	
yinfo = load_yaml(f"bangumi/{bangumi}.yaml" )

data = yinfo["tumi"]
items = len(data)

dirname = f"docs/{bangumi}"
os.makedirs(dirname, exist_ok=True)
generate_index(data, dirname=dirname)


# global meta
meta = yinfo['meta']
# episode = 1
# webseeds = yinfo['meta']['webseeds']
# episode = eval(webseeds['lambda'])
# print(webseeds['torrent'].format(episode=episode))

with open("all_maglinks.txt", "w") as fp:
	for i in range(items):
		prev_data = data[i-1] if i - 1 >= 0 else None
		next_data = data[i+1] if i + 1 < items else None
		curr_data = data[i]
		generate_bangumi(curr_data, meta, prev_data, next_data, dirname=dirname)
		# fp.write(curr_data["magnetlink"] + "&" + extra_trackers + "\n")
