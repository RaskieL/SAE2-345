DROP TABLE IF EXISTS liste_envie, commentaire, historique, note, ligne_panier, ligne_commande, commande, adresse, utilisateur, declinaison, gant, type_gant, etat, taille, couleur;

CREATE TABLE couleur(
   id_couleur INT NOT NULL AUTO_INCREMENT,
   libelle_couleur VARCHAR(255),
   code_couleur VARCHAR(255),
   PRIMARY KEY(id_couleur)
);

CREATE TABLE taille(
   id_taille INT NOT NULL AUTO_INCREMENT,
   num_taille_fr DECIMAL(3, 1),
   taille_us VARCHAR(255),
   tour_de_main DECIMAL(4, 1),
   PRIMARY KEY(id_taille)
);

CREATE TABLE etat(
   id_etat INT NOT NULL AUTO_INCREMENT,
   libelle VARCHAR(255),
   PRIMARY KEY(id_etat)
);

CREATE TABLE type_gant(
   id_type_gant INT NOT NULL AUTO_INCREMENT,
   nom_type_gant VARCHAR(255),
   PRIMARY KEY(id_type_gant)
);

CREATE TABLE gant(
   id_gant INT NOT NULL AUTO_INCREMENT,
   nom_gant VARCHAR(255),
   disponible BIT,
   poids VARCHAR(255),
   prix_gant DECIMAL(10, 2),
   description_gant VARCHAR(255),
   fournisseur VARCHAR(255),
   marque VARCHAR(255),
   image_gant VARCHAR(255),
   id_type_gant INT NOT NULL,
   PRIMARY KEY(id_gant),
   FOREIGN KEY(id_type_gant) REFERENCES type_gant(id_type_gant)
);

CREATE TABLE declinaison(
   id_declinaison INT NOT NULL AUTO_INCREMENT,
   stock INT,
   prix_declinaison DECIMAL(10, 2),
   id_couleur INT NOT NULL,
   id_taille INT NOT NULL,
   id_gant INT NOT NULL,
   PRIMARY KEY(id_declinaison),
   FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur),
   FOREIGN KEY(id_taille) REFERENCES taille(id_taille),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant)
);

CREATE TABLE utilisateur(
   id_utilisateur INT NOT NULL AUTO_INCREMENT,
   login VARCHAR(255),
   email VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   nom VARCHAR(255),
   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE adresse(
   id_adresse INT NOT NULL AUTO_INCREMENT,
   nom VARCHAR(255),
   rue VARCHAR(255),
   code_postal INT,
   ville VARCHAR(255),
   date_utilisation DATE,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_adresse),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE commande(
   id_commande INT NOT NULL AUTO_INCREMENT,
   date_achat DATE,
   id_etat INT NOT NULL,
   id_adresse INT NOT NULL,
   id_adresse_1 INT NOT NULL,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
   FOREIGN KEY(id_adresse) REFERENCES adresse(id_adresse),
   FOREIGN KEY(id_adresse_1) REFERENCES adresse(id_adresse),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE ligne_commande(
   id_declinaison INT,
   id_commande INT,
   quantite INT,
   prix DECIMAL(10, 2),
   PRIMARY KEY(id_declinaison, id_commande),
   FOREIGN KEY(id_declinaison) REFERENCES declinaison(id_declinaison),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
);

CREATE TABLE ligne_panier(
   id_declinaison INT,
   id_utilisateur INT,
   quantite INT,
   prix DECIMAL(10,2),
   nom VARCHAR(255),
   stock INT,
   PRIMARY KEY(id_declinaison, id_utilisateur),
   FOREIGN KEY(id_declinaison) REFERENCES declinaison(id_declinaison),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE note(
   id_gant INT,
   id_utilisateur INT,
   note VARCHAR(255),
   PRIMARY KEY(id_gant, id_utilisateur),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE historique(
   id_gant INT,
   id_utilisateur INT,
   date_consultation VARCHAR(255),
   PRIMARY KEY(id_gant, id_utilisateur, date_consultation),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE commentaire(
   id_gant INT,
   id_utilisateur INT,
   date_publication DATE,
   commentaire VARCHAR(255),
   valider BIT,
   PRIMARY KEY(id_gant, id_utilisateur, date_publication),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE liste_envie(
   id_gant INT,
   id_utilisateur INT,
   date_update DATE,
   PRIMARY KEY(id_gant, id_utilisateur, date_update),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
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

INSERT INTO couleur (libelle_couleur, code_couleur) VALUES
    ('Noir', '#000000'),
    ('Gris', '#D3D3D3'),
    ('Beige', '#F5F5DC'),
    ('Or', '#FFD700'),
    ('Orange', '#FF8000'),
    ('Rose', '#FD6C9E'),
    ('Rouge', '#FF0000'),
    ('Marron', '#582900'),
    ('Bleu', '0000FF'),
    ('Argent', 'C0C0C0'),
    ('Blanc', 'FFFFFF');

INSERT INTO gant (nom_gant, disponible, poids, prix_gant, description_gant, fournisseur, marque, image_gant, id_type_gant) VALUES
    ('Mouffles', 1, 50, 59.99, "Des mouffles d'une qualité exceptionnelle pour garder vos mains au chaud pendant l'hiver." ,'Wedze', 'Wedze', 'mouffle.png', 3),
    ('PowerGlove', 1, 500, 169.99, "Un gant d'une puissance absolue pour contrôler tous vos jeux à distance ! Plus jamais vous ne voudrez vous séparer du PowerGlove",'CDiscount', 'Nintendo', 'powerglove.png', 6),
    ('Gant de toilette', 1, 20, 1.49, "Un gant d'une grande douceur pour ne pas abîmer votre peau et garder une douceur de bébé.",'Linnea', 'Linnea', 'gant_de_toilette.png', 7),
    ('Gant de l infini', 1,  10000, 1999.99, "Prenez en main toute la puissance du gant de l'infini avec cette réplique grandeur nature et réaliste ! Tout est à votre portée !",'Nidavellir', 'Thanos', 'gauntlet_of_infinity.png', 6),
    ('Mitaines', 1, 20, 24.99, "Ces mitaines vous iront à ravir avec son style exceptionnel.",'Amazon', 'Satinior', 'mitaine.png', 2),
    ('Gants de cuisine', 1, 100, 6.99, "Ces gants de cuisines épais protègeront vos mains des chaleurs infernales de votre cuisine.",'Temu', 'Cuisinella', 'cuisine.png', 4),
    ('Gants de boxe', 1, 285, 23.50, "Pour boxer, n'hésiter plus, ces gants sont parfaits pour mettre enchaîner les crochets et les directs avec confort.",'Decathlon', 'Decathlon', 'gant_de_boxe.png', 5),
    ('Gants de moto', 1, 120, 17.99, "Ces gants de motos sont réalisés avec la maîtrise et l'artisanat d'ouvrier qualifiés basés en Arizona US. N'ayez plus peur d'affronter le goudron !",'Amazon', 'Westwood fox', 'moto.png', 4),
    ('Gants de gardien de but', 1, 110, 104.99, "Envie de réceptionner des ballons sur le terrain ? Alors ces gants sont parfaits pour vous ! Son cuir élégant vous protègera en tout confort",'Amazon', 'T1tan beast', 'foot.png', 5),
    ('Gants McDonnalds COLLECTOR 1987', 1, 25, 599.99, "Ces gants proviennent de la collection privée de Ronald McDonald's. Exclusivement produit en 4000 exemplaires en 1987, ce sont des gants collectors, disponibles seulement sur notre site en France.",'Ebay', 'McDonnalds', 'mcdo.png', 1),
    ('Gant de baseball', 1, 500, 39.99, "Le baseball n'aura plus de secret pour vous avec ces gants. Réceptionner toutes les balles, et ce avec confort et classe.",'Amazon', 'Barnett', 'baseball.png', 5),
    ('Manchettes-mitaines', 1, 30, 7.61, "Envie de confort et chaleur ? Ces manchettes-mitaines donneront une touche de féminité à votre style ravissant.",'Amazon', 'Bienvenu', 'femboy.png', 2),
    ('Gant gratte-chat', 1, 80, 3.49, "Votre chat vous fait chier ? Gratter le avec ce gant gratte-chat, et envoyez le au septième ciel !",'Amazon', 'Fousenuk', 'chat.png', 7),
    ('Gants de chevalier', 1, 1500, 819.99, "Envie de vous battre comme à Azincourt ? N'attendez plus et choisissez les gants de chevalier. Réalisés par un artisan médiéval authentique, ils vous protègeront des flèches et des épées !",'ArmStreet', 'ArmStreet', 'chevalier.png', 6),
    ('Gants d astronaute', 1, 460, 149.99, "Ces gants collectors sont des répliques fidèles aux gants d'astronautes qui ont posé le pied sur la Lune. N'attendez plus, et envolez vous vers les étoiles !",'Nasa', 'Nasa', 'astronaute.png', 7);

INSERT INTO declinaison (stock, prix_declinaison, id_couleur, id_taille, id_gant) VALUES
    (10, 59.99, 1, 3, 1),
    (5, 59.99, 1, 6, 1),
    (1, 169.99, 2, 6, 2),
    (18, 1.49, 3, 5, 3),
    (1, 1999.99, 4, 8, 4),
    (6, 24.99, 1, 1, 5),
    (6, 24.99, 1, 4, 5),
    (2, 6.99, 5, 7, 6),
    (2, 23.50, 6, 3, 7),
    (2, 23.99, 9, 6, 7),
    (6, 17.99, 1, 2, 8),
    (4, 104.99, 6, 4, 9),
    (1, 599.99, 7, 1, 10),
    (12, 39.99, 8, 7, 11),
    (20, 7.61, 6, 2, 12),
    (42, 3.49, 9, 5, 13),
    (2, 819.99, 10, 7, 14),
    (1, 149.99, 11, 6, 15);


INSERT INTO utilisateur(id_utilisateur, login, email, password, role, nom) VALUES
(1,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin'),
(2,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client'),
(3,'client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2');

INSERT INTO etat(id_etat, libelle) VALUES
(1,'en attente'),
(2,'expédié'),
(3,'validé'),
(4,'confirmé');

INSERT INTO adresse(nom, rue, code_postal, ville, date_utilisation, id_utilisateur)
VALUES
    ('Adresse Client', '123 Rue de la Ville', 75001, 'Paris', '2024-02-24', 2),
    ('Adresse Client2', '456 Rue de la Ville', 75002, 'Paris', '2024-02-25', 3);

INSERT INTO commande(date_achat, id_etat, id_adresse, id_adresse_1, id_utilisateur)
VALUES
    ('2024-02-24', 1, 1, 2, 2),
    ('2024-02-25', 2, 2, 1, 3);

INSERT INTO ligne_commande(id_declinaison, id_commande, quantite, prix)
VALUES
    (3, 1, 10, 169.99),
    (5, 2, 1, 24.99),
    (8, 2, 2, 13.98);
