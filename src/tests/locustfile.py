from locust import HttpUser, task, between
import random

class VolumeTestUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def listar_por_autor(self):
        self.client.get("/books/list/author?quantity=5")

class LoadTestUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def criar_livro(self):
        data = {
            "title": f"Livro Carga {random.randint(1, 100000)}",
            "publisher_id": 1,
            "cover_image": "http://example.com/image.jpg",
            "author_id": 1,
            "synopsis": "Teste de carga",
            "genre_id": 1
        }
        self.client.post("/books/", json=data)

    @task(1)
    def listar_por_autor(self):
        self.client.get("/books/list/author?quantity=5")

class StressTestUser(HttpUser):
    wait_time = between(0.1, 0.3)

    @task
    def criar_livro_stress(self):
        data = {
            "title": f"Livro Stress {random.randint(1, 100000)}",
            "publisher_id": 1,
            "cover_image": "http://example.com/image.jpg",
            "author_id": 1,
            "synopsis": "Teste de stress",
            "genre_id": 1
        }
        self.client.post("/books/", json=data)

    @task
    def listar_por_autor_stress(self):
        self.client.get("/books/list/author?quantity=5")
