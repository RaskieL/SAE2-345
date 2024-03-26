#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['GET','POST'])
def admin_commande_show():
    mycursor = get_db().cursor()
    sql_commandes = '''SELECT * FROM commande ORDER BY id_etat ASC'''
    mycursor.execute(sql_commandes)
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
    
    sql_user = '''SELECT login FROM utilisateur ORDER BY id_utilisateur ASC'''
    mycursor.execute(sql_user,)
    users = mycursor.fetchall()
    articles_commande = None
    adresse_livraison = None
    adresse_facturation = None

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
            
            sql = '''SELECT * FROM adresse JOIN commande ON commande.id_adresse = adresse.id_adresse WHERE commande.id_commande = %s;'''
            mycursor.execute(sql, (id_detail))
            adresse_livraison = mycursor.fetchone()
            sql = '''SELECT * FROM adresse JOIN commande ON commande.id_adresse_1 = adresse.id_adresse WHERE commande.id_commande = %s'''
            mycursor.execute(sql, (id_detail))
            adresse_facturation = mycursor.fetchone()

    if request.method == 'POST':
        commande_id = request.form.get('id_commande')
        if commande_id:
            sql_valider_commande = '''UPDATE commande SET etat_id = 2 WHERE id_commande = %s'''
            mycursor.execute(sql_valider_commande, (commande_id,))
            get_db().commit()
            return redirect('/admin/commande/show')
    return render_template('admin/commandes/show.html', commandes=commandes, users=users, articles_commande=articles_commande, adresse_livraison=adresse_livraison, adresse_facturation=adresse_facturation)

@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id:
        print(commande_id)
        sql_valider_commande = '''UPDATE commande SET id_etat = 2 WHERE id_commande = %s'''
        mycursor.execute(sql_valider_commande, (commande_id,))
        get_db().commit()
    return redirect('/admin/commande/show')