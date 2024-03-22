#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/article/commentaires', methods=['GET'])
def admin_article_details():
    mycursor = get_db().cursor()
    id_article =  request.args.get('id_article', None)
    
    sql = '''SELECT c.commentaire, u.nom, c.id_utilisateur, c.id_gant AS id_article,  c.date_publication, c.valider
    FROM commentaire c 
    INNER JOIN utilisateur u 
    ON c.id_utilisateur=u.id_utilisateur 
    WHERE id_gant=%s
    ORDER BY c.date_publication DESC;'''
    mycursor.execute(sql, ( id_article))
    commentaires = mycursor.fetchall()
    
    sql = '''SELECT id_gant as id_article, nom_gant as nom, prix_gant as prix, image_gant as image, description_gant as description
    FROM gant
    WHERE id_gant = %s;
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    return render_template('admin/article/show_article_commentaires.html'
                           , commentaires=commentaires
                           , article=article
                           )

@admin_commentaire.route('/admin/article/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''   DELETE FROM commentaire WHERE id_utilisateur=%s AND id_gant=%s AND date_publication LIKE %s   '''
    tuple_delete=(id_utilisateur,id_article,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)


@admin_commentaire.route('/admin/article/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_article = request.args.get('id_article', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/article/add_commentaire.html',id_utilisateur=id_utilisateur,id_article=id_article,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''   INSERT INTO commentaire VALUES
    (%s, %s, %s, %s, TRUE)'''
    mycursor.execute(sql, (id_article, id_utilisateur, date_publication, commentaire))
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)


@admin_commentaire.route('/admin/article/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_article = request.args.get('id_article', None)
    mycursor = get_db().cursor()
    sql = '''   UPDATE commentaire
    SET valider=TRUE
    WHERE id_gant=%s '''
    mycursor.execute(sql, (id_article))
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)