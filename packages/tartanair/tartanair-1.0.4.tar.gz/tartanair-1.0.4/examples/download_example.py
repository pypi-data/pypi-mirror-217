'''
Author: Yorai Shaoul
Date: 2023-02-03

Example script for downloading using the TartanAir dataset toolbox.
'''

# General imports.
import sys

# Local imports.
sys.path.append('..')
import tartanair as ta

# Create a TartanAir object.
tartanair_data_root = '/media/yoraish/overflow/data/tartanair-v2'
azure_token = "?sv=2021-10-04&ss=b&srt=sco&st=2023-07-04T14%3A49%3A25Z&se=2023-07-11T14%3A49%3A25Z&sp=rtl&sig=KrFc3KYTLiQFZOgQjdnJMiTNH495%2BjWYBgfXU3ghWqs%3D"
 
ta.init(tartanair_data_root, azure_token)

# Download a trajectory.
env = [
                "AmericanDinerExposure",
]
ta.download(env = env, difficulty = ['hard'], trajectory_id = ["P005"],  modality = ['image', 'imu'],  camera_name = ['lcam_front', 'lcam_left', 'lcam_right', 'lcam_back', 'lcam_top', 'lcam_bottom'])

# Can also download via a yaml config file.
# ta.download(config = 'download_config.yaml')
