DROP TABLE IF EXISTS gant, taille, type_gants;

CREATE TABLE utilisateur(
    id_utilisateur INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    identifiant VARCHAR(50),
    mot_de_passe VARCHAR(50),
    role_utilisateur VARCHAR,
    nom VARCHAR(50),
    email VARCHAR(50)
);


CREATE TABLE taille(
    id_taille INT,
    num_taille_fr INT,
    taille_us INT,
    tour_de_main INT,
    PRIMARY KEY (id_taille)

);

CREATE TABLE type_gant (
    id_type_gant INT,
    nom_type_gant VARCHAR(255),
    PRIMARY KEY (id_type_gant)

);

CREATE TABLE gant(
    id_gant INT AUTO_INCREMENT,
    nom_gant VARCHAR(255),
    poids INT,
    couleur VARCHAR(255),
    prix_gant VARCHAR(255),
    taille_id INT,
    type_gant_id INT,
    fournisseur VARCHAR(255),
    marque VARCHAR(255),
    PRIMARY KEY (id_gant),
    FOREIGN KEY (taille_id) REFERENCES taille(id_taille),
    FOREIGN KEY (type_gant_id) REFERENCES type_gant(id_type_gant)
);