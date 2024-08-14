class Settings:

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (54,69,79)


        self.ship_speed = 15

        #bullets settings
        self.bullet_speed = 4.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (47,47,47)

        #alien settings
        self.alien_speed = 1.0 
        self.fleet_drop_speed = 10

        #fleet direction 1 represents right  ; -1 left
        self.fleet_direction = 1 
