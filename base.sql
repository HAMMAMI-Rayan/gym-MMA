CREATE DATABASE mma_gym CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mma_gym;
CREATE TABLE membres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,  -- Correspond à l'ID de l'utilisateur dans la table User de Django
    date_naissance DATE NOT NULL,
    niveau_mma ENUM('Débutant', 'Intermédiaire', 'Avancé') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);
CREATE TABLE entraineurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    specialite VARCHAR(100) NOT NULL
);
CREATE TABLE cours (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    horaire TIME NOT NULL,
    entraineur_id INT NOT NULL,
    FOREIGN KEY (entraineur_id) REFERENCES entraineurs(id) ON DELETE CASCADE
);
CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    membre_id INT NOT NULL,
    cours_id INT NOT NULL,
    date_cours DATE NOT NULL,
    statut ENUM('en_attente', 'confirmée', 'annulée') NOT NULL DEFAULT 'en_attente',
    FOREIGN KEY (membre_id) REFERENCES membres(id) ON DELETE CASCADE,
    FOREIGN KEY (cours_id) REFERENCES cours(id) ON DELETE CASCADE
);
