def computeMetrics(diameters, image_frames):
    # convert frames to seconds assuming 60 fps
    timestamps = []
    for frame in image_frames:
        timestamps.append(frame / 60)

    velocity = []
    for i in range(1, len(timestamps)):
        if diameters[i] is None:
            continue
        velocity.append(abs(diameters[i] - diameters[i - 1]) / (timestamps[i] - timestamps[i - 1]))

    average_velocity = sum(velocity) / len(velocity)

    return average_velocity
