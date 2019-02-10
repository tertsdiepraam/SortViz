import pygame
pygame.init()

font = pygame.font.SysFont('Arial', 20)

class Dropdown:
    def __init__(self, options, position, default=None):
        self.options = options
        if default:
            self.selected = default
        else:
            self.selected = options[0] 
        self.open = False
        self.position = position
        self.rendered_texts = [font.render(option.replace('_', ' '), 1, (255, 255, 255)) for option in options]
        self.total_height = sum(x.get_rect().height for x in self.rendered_texts)
        self.total_width = max(x.get_rect().width for x in self.rendered_texts)
    
    def draw(self, screen):
        if self.open:
            screen.fill((0,0,0), pygame.Rect(*self.position, self.total_width, self.total_height))
            height = 0
            for text in self.rendered_texts:
                screen.blit(text, (self.position[0], self.position[1]+height))
                height += text.get_rect().height
        else:
            rendered_text = font.render(self.selected.replace('_', ' '), 1, (255, 255, 255))
            screen.fill((0,0,0), pygame.Rect(*self.position, self.total_width, rendered_text.get_rect().height))
            screen.blit(rendered_text, (self.position[0], self.position[1]))
    
    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.open:
                checking_rect = pygame.Rect(self.position[0], self.position[1], self.total_width, 0)
                for text, rendered in zip(self.options, self.rendered_texts):
                    checking_rect.height += rendered.get_rect().height
                    if checking_rect.collidepoint(pos):
                        self.selected = text
                        self.open = False
                        return self.selected
                    checking_rect.move((0, rendered.get_rect().height))
                self.open = False
            else:
                height = font.render(self.selected, 1, (255, 255, 255)).get_rect().height
                checking_rect = pygame.Rect(self.position[0], self.position[1], self.total_width, height)
                if checking_rect.collidepoint(pos):
                    self.open = True
        return False
                    