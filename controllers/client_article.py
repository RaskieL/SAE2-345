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

    # pour le filtre
    condition_and = ""
    sql = '''SELECT * FROM type_gant;'''
    sql2 = '''
    SELECT gant.id_gant as id_article,
    gant.nom_gant as nom,
    gant.prix_gant as prix,
    gant.image_gant as image,
    SUM(declinaison.stock) as stock,
    AVG(note.note) AS moy_notes,
    COUNT(DISTINCT note.note) AS nb_notes,
    COUNT(DISTINCT commentaire.commentaire) AS nb_avis
    FROM gant
    JOIN declinaison ON declinaison.id_gant = gant.id_gant
    LEFT JOIN note
    ON gant.id_gant=note.id_gant
    LEFT JOIN commentaire
    ON gant.id_gant=commentaire.id_gant
    '''

    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql2 += " WHERE "
    if "filter_word" in session:
        sql2 += "gant.nom_gant LIKE %s"
        recherche = "%" +session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql2 += condition_and + "gant.prix_gant BETWEEN %s AND %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = " AND "
    if "filter_types" in session:
        sql2 += condition_and + "("
        last_item = session["filter_types"][-1]
        for type in session["filter_types"]:
            sql2 += "gant.id_type_gant = %s "
            if type != last_item:
                sql2 += " OR "
            list_param.append(type)
        sql2 += ")"
    sql2 += " GROUP BY gant.id_gant;"
    tuple_sql = tuple(list_param)
    mycursor.execute(sql2, tuple_sql)
    print(sql2)
    articles = mycursor.fetchall()
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    # pour le panier
    sql = '''SELECT * FROM ligne_panier WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, (id_client))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql = '''SELECT SUM(ligne_panier.quantite * ligne_panier.prix) AS prix_total FROM ligne_panier WHERE ligne_panier.id_utilisateur = %s;'''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()['prix_total']
        print(prix_total)
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article
                           )
