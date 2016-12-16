1. Download and install TensorFlow
	https://www.tensorflow.org/get_started/os_setup
	
2. Train Neural Net
python graph.py --data_dir tweet_data --train_dir train_dir --size=256 --num_layers=2 --steps_per_checkpoint=30

3. Test inputs
	python graph.py --decode --data_dir tweet_data --train_dir train_dir --size=256 --num_layers=2

* note you can change size and num_layers, but they must be consistent between decode and train
** note train will run indefinitely, so you must manually stop the process
*** note sometimes Tweepy throws errors when grabbing data, usually stopping and re-running train will fix