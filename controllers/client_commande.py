#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT * FROM ligne_panier WHERE ligne_panier.id_utilisateur = %s;'''
    mycursor.execute(sql, (id_client))
    articles_panier = mycursor.fetchall()
    if len(articles_panier) >= 1:
        sql = '''SELECT SUM(ligne_panier.quantite * ligne_panier.prix) AS prix_total FROM ligne_panier WHERE ligne_panier.id_utilisateur = %s;'''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()['prix_total']
    else:
        prix_total = None
    # etape 2 : selection des adresses
    sql = '''SELECT * FROM adresse WHERE adresse.id_utilisateur = %s AND adresse.etat = 'VALIDE';'''
    mycursor.execute(sql, (id_client))
    adresses = mycursor.fetchall()

    sql = '''SELECT adresse.* FROM adresse JOIN adresse_favorite ON adresse_favorite.id_adresse = adresse.id_adresse WHERE adresse_favorite.id_utilisateur = %s;'''
    mycursor.execute(sql, (id_client,))
    adresse_fav = mycursor.fetchone()

    if adresse_fav is None:
        sql = '''SELECT * FROM adresse WHERE id_utilisateur = %s AND etat = 'VALIDE' ORDER BY nb_commande DESC LIMIT 1;'''
        mycursor.execute(sql, (id_client))
        adresse_fav = mycursor.fetchone()
        if adresse_fav is not None:
            new_adresse_fav = adresse_fav['id_adresse']
            sql = '''INSERT INTO adresse_favorite VALUES(%s,%s);'''
            mycursor.execute(sql, (id_client, new_adresse_fav))
            get_db().commit()
        else:
            return render_template('client/boutique/panier_validation_adresses.html'
                                    , adresses=adresses
                                    , articles_panier=articles_panier
                                    , prix_total= prix_total
                                    , validation=1
                                    )
        get_db().commit()
    
    return render_template('client/boutique/panier_validation_adresses.html'
                           , adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           , id_adresse_fav=adresse_fav['id_adresse']
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_adresse_livraison = request.form.get('id_adresse_livraison')
    id_adresse_facturation = request.form.get('id_adresse_facturation')
    adresse_identique = request.form.get('adresse_identique')
    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = '''SELECT * FROM ligne_panier WHERE ligne_panier.id_utilisateur = %s;'''
    mycursor.execute(sql, (id_client))
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
        return redirect('/client/article/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    if id_adresse_livraison is None or id_adresse_facturation is None:
        flash(u'Vous devez ajouter une adresse pour commander.', 'alert-warning')
        return redirect('/client/coordonnee/show')
    sql = '''INSERT INTO commande(date_achat, id_etat, id_adresse, id_adresse_1, id_utilisateur) VALUES (NOW(),%s,%s,%s,%s)'''
    if adresse_identique:
        mycursor.execute(sql, (1, id_adresse_livraison, id_adresse_livraison, id_client))
    else:
        mycursor.execute(sql, (1, id_adresse_livraison, id_adresse_facturation, id_client))
    
    sql = '''UPDATE adresse SET nb_commande = nb_commande+1 WHERE id_adresse = %s OR id_adresse = %s;'''
    mycursor.execute(sql, (id_adresse_livraison, id_adresse_facturation))
    get_db().commit()

    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    id_commande = mycursor.fetchone()
    # numéro de la dernière commande
    for item in items_ligne_panier:
        sql = '''SELECT quantite FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s;'''
        mycursor.execute(sql, (item['id_declinaison'], item['id_utilisateur']))
        qtCommandee = mycursor.fetchone()['quantite']
        sql = '''UPDATE declinaison SET stock = stock - %s WHERE id_declinaison = %s;'''
        mycursor.execute(sql, (qtCommandee ,item['id_declinaison']))
        sql = '''DELETE FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s;'''
        mycursor.execute(sql, (item['id_declinaison'], item['id_utilisateur']))
        sql =  '''INSERT INTO ligne_commande (id_declinaison, id_commande, quantite, prix) VALUES (%s, %s, %s, %s);'''
        mycursor.execute(sql, (item['id_declinaison'], id_commande['last_insert_id'], item['quantite'], item['prix']))

    sql = '''DELETE FROM adresse_favorite WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, (id_client))
    get_db().commit()

    sql = '''INSERT INTO adresse_favorite VALUES (%s,%s);'''
    mycursor.execute(sql, (id_client, id_adresse_livraison))
    get_db().commit()

    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql_commandes = '''
        SELECT * FROM commande
        WHERE id_utilisateur = %s
        ORDER BY id_etat ASC
    '''
    mycursor.execute(sql_commandes,(id_client,))
    commandes = mycursor.fetchall()

    for commande in commandes:
        mycursor.execute(
            'SELECT SUM(quantite) as total_quantite FROM ligne_commande WHERE id_commande = %s',
            (commande['id_commande'],)
        )
        sum_quantite = mycursor.fetchone()['total_quantite']
        commande['nbr_articles'] = sum_quantite

    for commande in commandes:
        mycursor.execute(
            'SELECT SUM(quantite) as total_quantite, SUM(prix) as total_prix FROM ligne_commande WHERE id_commande = %s',
            (commande['id_commande'],)
        )
        result = mycursor.fetchone()
        sum_quantite = result['total_quantite']
        sum_prix = result['total_prix']
        commande['nbr_articles'] = sum_quantite
        commande['prix_total'] = sum_prix

    articles_commande = None

    if request.method == 'GET':
        id_detail = request.args.get('id_commande', '')
        if id_detail:
            sql_commande_details = '''
                SELECT lc.quantite, lc.prix, d.id_declinaison, d.stock, d.prix_declinaison,
                    g.nom_gant, c.libelle_couleur, t.num_taille_fr, t.taille_us
                FROM ligne_commande lc
                JOIN declinaison d ON lc.id_declinaison = d.id_declinaison
                JOIN gant g ON d.id_gant = g.id_gant
                JOIN couleur c ON d.id_couleur = c.id_couleur
                JOIN taille t ON d.id_taille = t.id_taille
                WHERE lc.id_commande = %s
            '''
            mycursor.execute(sql_commande_details, (id_detail,))
            articles_commande = mycursor.fetchall()

    commande_adresse_livraison = None
    commande_adresse_facturation = None
    id_commande = request.args.get('id_commande', None)
    if id_commande:
        sql = ''' selection du détails d'une commande '''

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = '''SELECT * FROM adresse JOIN commande ON commande.id_adresse = adresse.id_adresse WHERE commande.id_commande = %s;'''
        mycursor.execute(sql, (id_commande))
        commande_adresse_livraison = mycursor.fetchone()
        print(commande_adresse_livraison)

        sql = '''SELECT * FROM adresse JOIN commande ON commande.id_adresse_1 = adresse.id_adresse WHERE commande.id_commande = %s;'''
        mycursor.execute(sql, (id_commande))
        commande_adresse_facturation = mycursor.fetchone()
        print(commande_adresse_livraison)

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresse_livraison=commande_adresse_livraison
                           , commande_adresse_facturation=commande_adresse_facturation
                           )

