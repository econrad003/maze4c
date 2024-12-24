# Make distance colormaps

all: gallery/dcm_sbt_50.png gallery/dcm_sbt_25.png gallery/dcm_sbt_75.png \
     gallery/dcm_sw_50.png gallery/dcm_sw_25.png gallery/dcm_sw_cs.png \
     gallery/dcm_iw_50.png gallery/dcm_iw_25.png gallery/dcm_iw_75.png \
     gallery/dcm_ow_50.png gallery/dcm_ow_25.png gallery/dcm_ow_75.png \
     gallery/dcm_vgt_dfs.png gallery/dcm_vgt_bfs.png \
     gallery/dcm_vgt_sprim.png gallery/dcm_vgt_vprim.png \
     gallery/dcm_kruskal.png gallery/dcm_wilson.png gallery/dcm_houston.png \
     gallery/dcm_eller.png gallery/dcm_eller_o.png gallery/dcm_huntkill.png

# HUNT AND KILL ALGORITHM
gallery/dcm_huntkill.png: demos/dcm_huntkill.py mazes/Algorithms/hunt_kill.py
	python -m demos.dcm_huntkill

# ELLER'S ALGORITHM
gallery/dcm_eller.png: demos/dcm_eller.py mazes/Algorithms/eller.py
	python -m demos.dcm_eller

gallery/dcm_eller_o.png: demos/dcm_eller.py mazes/Algorithms/outward_eller.py
	python -m demos.dcm_eller_o

# HOUSTON'S ALGORITHM
gallery/dcm_houston.png: demos/dcm_houston.py mazes/Algorithms/houston.py
	python -m demos.dcm_houston

# WILSON'S ALGORITHM
gallery/dcm_wilson.png: demos/dcm_wilson.py mazes/Algorithms/wilson.py
	python -m demos.dcm_wilson

# KRUSKAL'S ALGORITHM
gallery/dcm_kruskal.png: demos/dcm_kruskal.py mazes/Algorithms/kruskal.py
	python -m demos.dcm_kruskal

# VERTEX GROWING TREE
gallery/dcm_vgt_dfs.png: demos/dcm_vgt_dfs.py mazes/Algorithms/growing_tree1.py mazes/Queues/stack.py
	python -m demos.dcm_vgt_dfs

gallery/dcm_vgt_bfs.png: demos/dcm_vgt_bfs.py mazes/Algorithms/growing_tree1.py mazes/Queues/queue.py
	python -m demos.dcm_vgt_bfs

gallery/dcm_vgt_sprim.png: demos/dcm_vgt_sprim.py mazes/Algorithms/growing_tree1.py mazes/Queues/random_queue.py
	python -m demos.dcm_vgt_sprim

gallery/dcm_vgt_vprim.png: demos/dcm_vgt_vprim.py mazes/Algorithms/growing_tree1.py mazes/Queues/priority_queue.py
	python -m demos.dcm_vgt_vprim

# OUTWINDER
gallery/dcm_ow_75.png: demos/dcm_ow_75.py mazes/Algorithms/outwinder.py
	python -m demos.dcm_ow_75

gallery/dcm_ow_25.png: demos/dcm_ow_25.py mazes/Algorithms/outwinder.py
	python -m demos.dcm_ow_25

gallery/dcm_ow_50.png: demos/dcm_ow_50.py mazes/Algorithms/outwinder.py
	python -m demos.dcm_ow_50

# INWINDER
gallery/dcm_iw_75.png: demos/dcm_iw_75.py mazes/Algorithms/inwinder.py
	python -m demos.dcm_iw_75

gallery/dcm_iw_25.png: demos/dcm_iw_25.py mazes/Algorithms/inwinder.py
	python -m demos.dcm_iw_25

gallery/dcm_iw_50.png: demos/dcm_iw_50.py mazes/Algorithms/inwinder.py
	python -m demos.dcm_iw_50

# SIDEWINDER
gallery/dcm_sw_cs.png: demos/dcm_sw_cs.py mazes/Algorithms/sidewinder.py
	python -m demos.dcm_sw_cs

gallery/dcm_sw_25.png: demos/dcm_sw_25.py mazes/Algorithms/sidewinder.py
	python -m demos.dcm_sw_25

gallery/dcm_sw_50.png: demos/dcm_sw_50.py mazes/Algorithms/sidewinder.py
	python -m demos.dcm_sw_50

# SIMPLE BINARY TREE
gallery/dcm_sbt_75.png: demos/dcm_sbt_75.py mazes/Algorithms/simple_binary_tree.py
	python -m demos.dcm_sbt_75

gallery/dcm_sbt_25.png: demos/dcm_sbt_25.py mazes/Algorithms/simple_binary_tree.py
	python -m demos.dcm_sbt_25

gallery/dcm_sbt_50.png: demos/dcm_sbt_50.py mazes/Algorithms/simple_binary_tree.py
	python -m demos.dcm_sbt_50

