import math


def reward_function(params):
    """
    Example of rewarding the agent to follow center line
    """

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    steering_angle = params['steering_angle']
    speed = params['speed']

    # Initialize the reward with typical value
    reward = 1.0

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    x2 = next_point[0]
    y2 = next_point[1]
    x1 = prev_point[0]
    y1 = prev_point[1]

    car_direction = heading + steering_angle
    # comparing the angle between the previous way point and the next waypoint with the car direction
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

    future_point = waypoints[closest_waypoints[1] + 2]
    x4 = future_point[0]
    y4 = future_point[1]

    # if track up ahead is straight then reward faster speeds
    angle_ahead = math.atan((x4 - x2) / (y4 - y2))
    if abs(angle - angle_ahead) < 1:
        if speed > 3.0:
            reward *= 1.5

    return float(reward)
