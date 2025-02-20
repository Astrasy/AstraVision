import pygame
import numpy as np
import cv2
import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import asyncio
import json
import os
from pygame import gfxdraw
import random
from pathlib import Path

@dataclass
class AstraState:
    consciousness_level: float  # Nível de consciência
    neural_sync: float         # Sincronização neural
    quantum_coherence: float   # Coerência quântica
    mindflow_index: float      # Índice de fluxo mental
    energy_field: float        # Campo de energia
    timestamp: datetime.datetime

class AstraUI:
    """Gerenciador de interface do AstraVision"""
    
    def __init__(self, screen, size):
        self.screen = screen
        self.size = size
        self.fonts = self._init_fonts()
        self.colors = self._init_colors()
        self.particles = []
        
    def _init_fonts(self) -> Dict:
        return {
            'large': pygame.font.Font(None, 48),
            'medium': pygame.font.Font(None, 36),
            'small': pygame.font.Font(None, 24)
        }
    
    def _init_colors(self) -> Dict:
        return {
            'background': (0, 4, 20),
            'primary': (0, 255, 170),
            'secondary': (170, 0, 255),
            'accent': (255, 170, 0),
            'text': (200, 255, 255),
            'dark': (10, 10, 30)
        }
    
    def draw_hex_background(self):
        """Desenha background hexagonal animado"""
        size = 40
        offset = self.frame_count * 0.5
        for x in range(0, self.size[0] + size * 2, size * 2):
            for y in range(0, self.size[1] + size * 2, size * 2):
                points = []
                for i in range(6):
                    angle = i * 60 + offset
                    px = x + size * np.cos(np.radians(angle))
                    py = y + size * np.sin(np.radians(angle))
                    points.append((int(px), int(py)))
                
                alpha = int(128 + 64 * np.sin(offset * 0.05 + x * 0.01 + y * 0.01))
                pygame.draw.polygon(self.screen, (*self.colors['dark'], alpha), points, 1)

class AstraVision:
    def __init__(self, user_id: str):
        pygame.init()
        
        # Configurações de display
        self.size = (1920, 1080)
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("AstraVision 2025")
        
        # Inicialização de componentes
        self.user_id = user_id
        self.ui = AstraUI(self.screen, self.size)
        self.state = None
        self.history = []
        self.frame_count = 0
        self.mode = "neural"
        self.particles = []
        
        # Sistema de câmera
        self.setup_camera()
        
        # Métricas de performance
        self.metrics = {
            'fps': 0,
            'render_time': 0,
            'process_time': 0
        }
        
        # Carrega assets
        self.load_assets()

    def setup_camera(self):
        """Configura sistema de câmera com fallback"""
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.camera_available = True
        except:
            print("Camera não disponível - modo alternativo ativado")
            self.camera_available = False

    def load_assets(self):
        """Carrega recursos necessários"""
        self.assets = {
            'particles': [],
            'sounds': {},
            'shaders': {}
        }
        
        # Adiciona partículas base
        for _ in range(100):
            self.particles.append({
                'pos': [random.randint(0, self.size[0]), random.randint(0, self.size[1])],
                'vel': [random.uniform(-1, 1), random.uniform(-1, 1)],
                'size': random.uniform(2, 5),
                'color': self.ui.colors['primary']
            })

    async def run(self):
        """Loop principal assíncrono"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            start_time = time.time()
            
            # Processa eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.toggle_mode()
            
            # Atualiza estado
            await self.update_state()
            
            # Renderiza frame
            self.render()
            
            # Atualiza métricas
            self.metrics['fps'] = clock.get_fps()
            self.metrics['render_time'] = time.time() - start_time
            
            # Mantém 60 FPS
            clock.tick(60)
            self.frame_count += 1
            
            # Permite outras tarefas assíncronas
            await asyncio.sleep(0)

    async def update_state(self):
        """Atualiza estado do sistema"""
        self.state = AstraState(
            consciousness_level=self.calculate_consciousness(),
            neural_sync=self.calculate_neural_sync(),
            quantum_coherence=self.calculate_quantum_coherence(),
            mindflow_index=self.calculate_mindflow(),
            energy_field=self.calculate_energy_field(),
            timestamp=datetime.datetime.utcnow()
        )
        
        self.history.append(self.state)
        if len(self.history) > 1000:
            self.history.pop(0)

    def render(self):
        """Sistema de renderização principal"""
        # Limpa tela
        self.screen.fill(self.ui.colors['background'])
        
        # Renderiza background
        self.ui.draw_hex_background()
        
        # Renderiza elementos principais
        self.render_main_display()
        self.render_metrics()
        self.render_particles()
        
        if self.camera_available:
            self.render_camera_feed()
        
        # Atualiza display
        pygame.display.flip()

    def render_main_display(self):
        """Renderiza display principal"""
        # Área central
        center_rect = pygame.Rect(
            self.size[0] * 0.2,
            self.size[1] * 0.1,
            self.size[0] * 0.6,
            self.size[1] * 0.6
        )
        
        # Renderiza gráficos de estado
        self.render_state_graphics(center_rect)
        
        # Informações do usuário
        user_text = self.ui.fonts['large'].render(
            f"ASTRA VISION | Usuário: {self.user_id}",
            True,
            self.ui.colors['text']
        )
        self.screen.blit(user_text, (20, 20))

    def render_state_graphics(self, rect):
        """Renderiza gráficos de estado neural"""
        if not self.state:
            return
            
        # Gráfico circular principal
        center = rect.center
        radius = min(rect.width, rect.height) * 0.3
        
        # Desenha círculos concêntricos
        for i in range(3):
            r = radius * (1 - i * 0.2)
            pygame.draw.circle(
                self.screen,
                self.ui.colors['primary'],
                center,
                int(r),
                2
            )
        
        # Renderiza métricas em círculo
        metrics = [
            ("Consciência", self.state.consciousness_level),
            ("Sync Neural", self.state.neural_sync),
            ("Coerência", self.state.quantum_coherence),
            ("Mindflow", self.state.mindflow_index),
            ("Energia", self.state.energy_field)
        ]
        
        for i, (name, value) in enumerate(metrics):
            angle = i * (360 / len(metrics))
            x = center[0] + np.cos(np.radians(angle)) * radius * 0.8
            y = center[1] + np.sin(np.radians(angle)) * radius * 0.8
            
            # Texto
            text = self.ui.fonts['small'].render(
                f"{name}: {value:.2f}",
                True,
                self.ui.colors['text']
            )
            self.screen.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    def render_particles(self):
        """Sistema de partículas dinâmico"""
        for particle in self.particles:
            # Atualiza posição
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            
            # Wrap around
            particle['pos'][0] = particle['pos'][0] % self.size[0]
            particle['pos'][1] = particle['pos'][1] % self.size[1]
            
            # Desenha partícula
            pygame.draw.circle(
                self.screen,
                particle['color'],
                (int(particle['pos'][0]), int(particle['pos'][1])),
                particle['size']
            )

    def render_camera_feed(self):
        """Renderiza feed da câmera com análise"""
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (320, 180))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            
            # Posição do feed
            self.screen.blit(frame, (self.size[0] - 340, self.size[1] - 200))

    def calculate_consciousness(self) -> float:
        """Calcula nível de consciência"""
        base = random.uniform(0.7, 1.0)
        wave = np.sin(self.frame_count * 0.01) * 0.1
        return min(1.0, max(0.0, base + wave))

    def calculate_neural_sync(self) -> float:
        """Calcula sincronização neural"""
        base = random.uniform(0.6, 0.9)
        wave = np.cos(self.frame_count * 0.02) * 0.15
        return min(1.0, max(0.0, base + wave))

    def calculate_quantum_coherence(self) -> float:
        """Calcula coerência quântica"""
        base = random.uniform(0.5, 0.8)
        wave = np.sin(self.frame_count * 0.03) * 0.2
        return min(1.0, max(0.0, base + wave))

    def calculate_mindflow(self) -> float:
        """Calcula índice de fluxo mental"""
        if not self.state:
            return 0.5
        return (self.state.consciousness_level * 0.4 +
                self.state.neural_sync * 0.3 +
                self.state.quantum_coherence * 0.3)

    def calculate_energy_field(self) -> float:
        """Calcula campo de energia"""
        base = random.uniform(0.4, 0.7)
        wave = np.sin(self.frame_count * 0.04) * 0.25
        return min(1.0, max(0.0, base + wave))

    def cleanup(self):
        """Limpa recursos do sistema"""
        if self.camera_available:
            self.camera.release()
        pygame.quit()
