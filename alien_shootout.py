import sys 
import pygame 


from pygame.sprite import Sprite
from settings import Settings
from aliens import Alien
from button import Button

from ship import Ship
from bullets import Bullet
class Alien_Shootout :
    """Class assests and behaviours."""
    def __init__(self):
        pygame.init()
        self.settings=Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings.screen_width ,self.settings.screen_height))
        pygame.display.set_caption("Alein Shootout")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.game_active = True
        self.play_button = Button(self, "Play")
        

    def run_game(self) :
        while True:
            self._check_events()
            if self.game_active :

                self.ship.update()
                self._update_bullets()  
                self._update_aliens()
            self._update_screen()
 
            self.clock.tick(60)
            pygame.display.flip()
    
    def _check_events(self):

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN :
                    self.keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self.keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos) 
               

    def keydown_events(self,event) :
        if event.key == pygame.K_RIGHT :
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT :
            self.ship.moving_left = True
        elif event.key == pygame.K_q :
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        
    def keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self) :
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
             
             
        self.ship.blitme()
        self.aliens.draw(self.screen)

        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()
    
    def _update_bullets(self):
        self.bullets.update()

         #Get rid the bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):

        #check for any bullet hit the aliens.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            #destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()


    def _create_fleet(self) :
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y =alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        #looking for alien - ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Opps ,Game End!!!")
            self.game_active = False
            self.bullets.empty()
            self.aliens.empty()

            #creating new ship and center it.
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(True)
            

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._check_fleet_direction()
                break

    def _check_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked:
           self.game_active = True
           pygame.mouse.set_visible(False)     

                

if __name__=='__main__' :
    ai = Alien_Shootout()
    ai.run_game()


