import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Teste: Listar atividades

def test_get_activities():
    # Arrange
    # (nenhuma preparação extra necessária)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data or "Clube de Xadrez" in data

# Teste: Inscrever aluno em uma atividade

def test_signup_activity():
    # Arrange
    email = "novoaluno@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

# Teste: Prevenir duplicidade de inscrição

def test_signup_duplicate():
    # Arrange
    email = "duplicado@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# Teste: Remover participante

def test_remove_participant():
    # Arrange
    email = "remover@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]

# Teste: Remover participante inexistente

def test_remove_nonexistent_participant():
    # Arrange
    email = "naoexiste@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

# Teste: Atividade inexistente

def test_signup_nonexistent_activity():
    # Arrange
    email = "aluno@mergington.edu"
    activity = "Atividade Fantasma"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
