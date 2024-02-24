#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,

                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    list_param = []

    sql = '''SELECT gant.id_gant as id_article,
    nom_gant as nom,
    prix_gant as prix,
    image_gant as image,
    SUM(declinaison.stock) as stock
    FROM gant
    JOIN declinaison ON declinaison.id_gant = gant.id_gant
    GROUP BY gant.id_gant;'''
    mycursor.execute(sql)
    articles = mycursor.fetchall()

    # pour le filtre
    sql = '''SELECT * FROM type_gant;'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    # pour le panier
    sql = '''SELECT * FROM ligne_panier WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, (id_client))
    articles_panier = mycursor.fetchall()
    print("article ??")
    for article in articles_panier:
        print(article)

    if len(articles_panier) >= 1:
        #sql = '''SELECT SUM(declinaison.prix_declinaison) FROM ligne_panier WHERE ligne_panier.id_utilisateur = %s JOIN declinaison ON ligne_panier.id_declinaison = declinaison.id_declinaison GROUP BY ligne_panier.id_declinaison;'''
        #mycursor.execute(sql, id_client)
        prix_total = None
        #print("prix ??")
        #print(prix_total)
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , items_filtre=types_article
                           )
