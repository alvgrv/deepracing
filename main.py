import math


def reward_function(params):
    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    steering_angle = params['steering_angle']
    speed = params['speed']
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']

    # Initialize the reward with typical value
    reward = 1.0

    if distance_from_center > (track_width/2*0.75):
        reward *= 0.75

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    x2 = next_point[0]
    y2 = next_point[1]
    x1 = prev_point[0]
    y1 = prev_point[1]

    car_direction = heading + steering_angle
    # comparing the angle between the previous way point and the next waypoint with the car direction
    if y2 - y1 == 0:
        angle = 0
        direction_diff = 0 - car_direction
    else:
        angle = math.atan((x2 - x1) / (y2 - y1))
        if x2 > x1 and y2 > y1:
            direction_diff = angle - car_direction
        elif x2 < x1 and y2 > y1:
            direction_diff = (angle + 90) - car_direction
        elif x2 < x1 and y2 < y1:
            direction_diff = (angle + 90) - abs(car_direction)
        else:
            direction_diff = angle - abs(car_direction)

    ALLOWED_DIFF = 10
    if abs(direction_diff) > ALLOWED_DIFF:
        reward *= 0.5

    if not all_wheels_on_track:
        reward *= 0.5

    try:
        future_point = waypoints[closest_waypoints[1] + 1]
    except IndexError:
        return float(reward)

    x3 = future_point[0]
    y3 = future_point[1]

    # if track up ahead is straight then reward faster speeds
    if y3 - y2 == 0:
        angle_ahead = 0
    else:
        angle_ahead = math.atan((x3 - x2) / (y3 - y2))

    if abs(angle - angle_ahead) < 1:
        if speed > 3.0:
            reward *= 1.5

    return float(reward)