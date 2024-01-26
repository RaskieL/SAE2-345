DROP TABLE IF EXISTS ligne_commande, ligne_panier, commande, etat, gant, taille, type_gant, utilisateur;

CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(255),
   email VARCHAR(255),
   nom VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE taille(
    id_taille INT AUTO_INCREMENT,
    num_taille_fr DECIMAL(3, 1),
    taille_us VARCHAR(15),
    tour_de_main DECIMAL(3, 1),
    PRIMARY KEY (id_taille)
);

CREATE TABLE type_gant (
    id_type_gant INT AUTO_INCREMENT,
    nom_type_gant VARCHAR(255),
    PRIMARY KEY (id_type_gant)
);

CREATE TABLE gant(
    id_gant INT AUTO_INCREMENT,
    nom_gant VARCHAR(255),
    poids INT,
    couleur VARCHAR(255),
    prix_gant DECIMAL(10, 2),
    taille_id INT,
    type_gant_id INT,
    fournisseur VARCHAR(255),
    marque VARCHAR(255),
    image_gant VARCHAR(255),
    PRIMARY KEY (id_gant),
    FOREIGN KEY (taille_id) REFERENCES taille(id_taille),
    FOREIGN KEY (type_gant_id) REFERENCES type_gant(id_type_gant)
);

CREATE TABLE etat(
   id_etat INT,
   libelle VARCHAR(255),
   PRIMARY KEY(id_etat)
);

CREATE TABLE commande(
   id_commande INT,
   date_achat DATE,
   utilisateur_id INT NOT NULL,
   etat_id INT NOT NULL,
   id_etat INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat)
);

CREATE TABLE ligne_panier(
   id_gant INT,
   id_utilisateur INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(id_gant, id_utilisateur),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE ligne_commande(
   id_gant INT,
   id_commande INT,
   prix DECIMAL(10,2),
   quantite INT,
   PRIMARY KEY(id_gant, id_commande),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
);

INSERT INTO taille (num_taille_fr, taille_us, tour_de_main) VALUES
    (6.5, 'S (F)', 17.5),
    (7, 'M (F)', 19),
    (7.5, 'L (F)', 20),
    (8, 'XL (F)', 21.5),
    (8.5, 'M (H)', 23),
    (9, 'L (H)', 24),
    (9.5, 'XL (H)', 25.5),
    (10, 'XXL (H)', 27);

INSERT INTO type_gant (nom_type_gant) VALUES
    ('Original'),
    ('Mitaine'),
    ('Mouffle'),
    ('Protection'),
    ('Sport'),
    ('Fantaisie'),
    ('Autre');

INSERT INTO gant (nom_gant, poids, couleur, prix_gant, taille_id, type_gant_id, fournisseur, marque, image_gant) VALUES
    ('Mouffles', 50, 'Noir', 59.99, 6, 3, 'Wedze', 'Wedze', 'mouffle.png'),
    ('PowerGlove', 500, 'Gris', 169.99, 3, 6, 'CDiscount', 'Nintendo', 'powerglove.png'),
    ('Gant de toilette', 20, 'Beige', 1.49, 8, 7, 'Linnea', 'Linnea', 'gant_de_toilette.png'),
    ('Gant de l infini',  10000, 'Or', 99999999.99, 8, 6, 'Nidavellir', 'Thanos', 'gauntlet_of_infinity.png'),
    ('Mitaines', 20, 'Noir', 24.99, 4, 2, 'Amazon', 'Satinior', 'mitaine.png'),
    ('Gants de cuisine', 100, 'Orange', 6.99, 8, 4, 'Temu', 'Cuisinella', 'cuisine.png'),
    ('Gants de boxe', 285, 'Rose', 23.50, 6, 5, 'Decathlon', 'Decathlon', 'gant_de_boxe.png'),
    ('Gants de moto', 120, 'Noir', 17.99, 7, 4, 'Amazon', 'Westwood fox', 'moto.png'),
    ('Gants de gardien de but', 110, 'Rouge', 104.99, 6, 5, 'Amazon', 'T1tan beast', 'foot.png'),
    ('Gants McDonnalds COLLECTOR 1987', 25, 'Rouge', 599.99, 1, 1, 'Ebay', 'McDonnalds', 'mcdo.png'),
    ('Gant de baseball', 500, 'Marron', 39.99, 5, 5, 'Amazon', 'Barnett', 'baseball.png'),
    ('Manchettes-mitaines', 30, 'Rose', 7.61, 2, 2, 'Amazon', 'Bienvenu', 'femboy.png'),
    ('Gant gratte-chat', 80, 'Bleu', 3.49, 5, 7, 'Amazon', 'Fousenuk', 'chat.png'),
    ('Gants de chevalier', 1500, 'Argent', 819.99, 7, 6, 'ArmStreet', 'ArmStreet', 'chevalier.png'),
    ('Gants d astronaute', 460, 'Blanc', 14999999.99, 6, 7, 'Nasa', 'Nasa', 'astronaute.png');