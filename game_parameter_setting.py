#set the game options
FPS = 30 #run the game at rate FPS, the speed at which images are shown
max_score = 100 #the maximum score of the game before we break the loop

#floor options
floor_velocity = 5 #the horizontal moving velocity of the floor, this should equal to pipe_velocity
floor_starting_y_position = 500 #the starting y position of the floor

#pipe options
pipe_max_num = 100 #the maximum number of pipes in this game
pipe_vertical_gap = 170 #the gap between the top pipe and the bottom pipe, the smaller the number, the harder the game
pipe_horizontal_gap = 200 #the gap between two sets of pipes
pipe_velocity = 5 #the horizontal moving velocity of the pipes, this should equal to floor_velocity
top_pipe_min_height = 100 #the minimum height of the top pipe (carefully set this number)
top_pipe_max_height = 300 #the maximum height of the top pipe (carefully set this number)
pipe_starting_x_position = 500 #the starting x position of the first pipe

#bird options
bird_max_upward_angle = 35 #the maximum upward angle when flying up
bird_max_downward_angle = -90 #the maximum downward angle when flying down
bird_min_incremental_angle = 5 #the minimum incremental angle when tilting up or down
bird_angular_acceleration = 0.3 #the acceleration of bird's flying angle
bird_jump_velocity = -8 #the vertical jump up velocity
bird_acceleration = 3 #the gravity for the bird in the game
bird_max_displacement = 12 #the maximum displacement per frame
bird_starting_x_position = 150 #the starting x position of the bird
bird_starting_y_position = 250 #the starting y position of the bird