import airsim

client = airsim.MultirotorClient()

client.confirmConnection()

client.enableApiControl(True)
client.armDisarm(True)



client.takeoffAsync().join()

client.moveToPositionAsync(0, 0,-2, 10,yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=90),drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom).join()

client.reset()
