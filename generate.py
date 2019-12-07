import yaml
from jinja2 import Environment, FileSystemLoader
import os

extra_trackers="&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com"

def load_yaml( filename ):
	with open( filename, 'rb' ) as f:
		return yaml.load( f, Loader=yaml.FullLoader)

def generate_bangumi(curr_data, prev_data=None, next_data=None, extra_trackers=extra_trackers):
	env = Environment(
		loader=FileSystemLoader( os.path.dirname(os.path.abspath(__file__)) ),
		trim_blocks=True )
	template = env.get_template('template_bangumi.html')
	'''
	data:
		magnetlink:
		torrent:
		name:
	'''
	# prev_id, curr_id, next_id = ("ep-%d.html" % (index + i) for i in (-1, 0, 1))
	curr_id = curr_data["episode"]
	bangumi = {
		"name" : "Kimestu no Yaiba",
	}
	htmlpage = template.render(
			prev=prev_data, 
			curr=curr_data, 
			next=next_data, 
			extra_trackers=extra_trackers,
			bangumi=bangumi
		)
	
	filename = "docs/ep-%s.html" % curr_id
	with open(filename, 'w') as f:
		f.write(htmlpage)
		print("Successfuly generate_bangumi %s" % filename)

def generate_index(bangumi):
	env = Environment(
		loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) ),
		trim_blocks=True )
	template = env.get_template('template_index.html')

	htmlpage = template.render(
			bangumi=bangumi
		)
	
	filename = "docs/index.html"
	with open(filename, 'w') as f:
		f.write(htmlpage)
		print("Successfuly generate_index %s" % filename)
	
data = load_yaml( "bangumi.yaml" )
items = len(data)
generate_index(data)
for i in range(items):
	prev_data = data[i-1] if i - 1 >= 0 else None
	next_data = data[i+1] if i + 1 < items else None
	curr_data = data[i]
	generate_bangumi(curr_data, prev_data, next_data)



