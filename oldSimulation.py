# INITIALIZING ==============================
# sets the initial condition for the loop


for i in range(len(bodies)):                    # starts at index 0 and itterates through each body in bodies

    body1 = bodies[i]    

    if i+1 != len(bodies):                      # if last body in list, no more acceleration is added
        for j in range(i+1, len(bodies)):       # starts at index

            body2 = bodies[j]


            # CALCULATING ==============================
            # BODY 1 AND BODY 2's CHANGE IN ACCELERATION

            # creating the line and storing its direction and magnitude
            line_1_2 = V.Vector(body2.position.x - body1.position.x, body2.position.y - body1.position.y)
            unit_1_2 = line_1_2.normalize()
            r_btw = line_1_2.magnitude()

            # acceleration calculated and stored
            acc_on_1 = (G * body2.mass) / (r_btw**2)
            body1.cur_ac.x += unit_1_2.x * acc_on_1
            body1.cur_ac.y += unit_1_2.y * acc_on_1

            # acceleration calculated and stored
            acc_on_2 = (G * body1.mass) / (r_btw**2)
            body2.cur_ac.x += -1 * unit_1_2.x * acc_on_2
            body2.cur_ac.y += -1 * unit_1_2.y * acc_on_2
            



# ITERATING ==============================
# moves through the established time loop

for time in range(0, total_time, dt):

    for i in range(len(bodies)):
        body1 = bodies[i]


        # UPDATING ==============================
        # BODY-1's POSITION

        # Updates the position of Body 1

        # temporary storage of change in position for current body
        change_in_position = V.Vector(0,0)
        change_in_position.x += (body1.velocity.x * dt + 0.5 * body1.cur_ac.x * dt**2)
        change_in_position.y += (body1.velocity.y * dt + 0.5 * body1.cur_ac.y * dt**2)

        # updates the current bodies position
        body1.position.x += change_in_position.x
        body1.position.y += change_in_position.y

        # resetting escaped states to True
        body1.escaped = True;





    # ITERATING ==============================
    # OUTER FOR LOOP - moves once through all bodies in the system under alias body1
    # INNER FOR LOOP - moves through bodies after body1 under alias body2

    for i in range(len(bodies)):                    # starts at index 0 and itterates through each body in bodies

        body1 = bodies[i]

        # conditional variables
        collided = False    # Will flag as True and kill the simulation if two bodies collide
        PE = 0 

                     
        if i+1 != len(bodies):                      # if last body in list, no more acceleration is added
            for j in range(i+1, len(bodies)):       # starts at index
                body2 = bodies[j]

            
                # CALCULATING ==============================
                # BODY 1 AND BODY 2's CHANGE IN ACCELERATION

                # creating the line and storing its direction and magnitude
                line_1_2 = V.Vector(body2.position.x - body1.position.x, body2.position.y - body1.position.y)
                unit_1_2 = line_1_2.normalize()
                r_btw = line_1_2.magnitude()

                # CONDITION ==============================
                # HAVE BODY 1 AND BODY 2 COLLIDED?
                if (body1.radius + body2.radius) > r_btw:
                    print(f'Bodies have collided. Simulation over.')
                    sys.exit
                    

                # DOES BODY 1 ESCAPE FROM BODY 2?
                    # ALSO MEANS BODY 2 WILL ESCAPE FROM BODY 1
                
                if body1.velocity.magnitude() < ap.escape_velocity(G * body2.mass, r_btw):
                    body1.escaped = False
                    body2.escaped = False


                

                # next acceleration calculated and stored
                acc_on_1 = (G * body2.mass) / (r_btw**2)
                body1.nxt_ac.x += unit_1_2.x * acc_on_1
                body1.nxt_ac.y += unit_1_2.y * acc_on_1

                # next acceleration calculated and stored
                acc_on_2 = (G * body1.mass) / (r_btw**2)
                body2.nxt_ac.x += -1 * unit_1_2.x * acc_on_2
                body2.nxt_ac.y += -1 * unit_1_2.y * acc_on_2
            

        # CALCULATING AND UPDATING ==============================
        # BODY 1's CHANGE IN VELOCITY


        # changes in velocity
        body1.velocity.x += 0.5 * dt * (body1.cur_ac.x + body1.nxt_ac.x)
        body1.velocity.y += 0.5 * dt * (body1.cur_ac.y + body1.nxt_ac.y)

        
        # TEST CASE: CONSERVATION OF ENERGY
        
        PE = -1 * body1.mass * body1.cur_ac.magnitude() * change_in_position.magnitude()

        KE = 0.5 * body1.mass * body1.velocity.magnitude()**2

        total_energy = PE + KE

        print(total_energy)


        # CONDITION ==============================
        # DID THIS BODY LEAVE THE SYSTEM

        if body1.escaped == True:       # checks if the flag didnt trigger
            bodies.remove(body1)
            print (f'Body has escaped and has left the system')
            sys.exit()

        

        # RESETTING ==============================
        # sets the current acceleration to the value of the next acceleration
        # resets the nxt_ac to 0


        body1.cur_ac.x = body1.nxt_ac.x
        body1.cur_ac.y = body1.nxt_ac.y
        body1.nxt_ac = V.Vector(0, 0)

        
        



    #============================================================#
    #============================================================#
    # YOU CAN NOW SAVE THE DATA


