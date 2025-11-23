import flask
from errors import HttpError
from models import Session, Ann
from flask import jsonify,request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from schema import AnnouncementCreate, AnnouncementUpdate, validate_json
app = flask.Flask("app")

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    request.session.close()
    return response

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'error': error.message})
    http_response.status_code = error.status_code
    return http_response


def get_ann_by_id(ann_id):
    announcement = request.session.get(Ann, ann_id)
    if announcement is None:
        raise HttpError(404, 'Announcement not found')
    return announcement

def add_ann(announcement):
    try:
        request.session.add(announcement)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, 'Announcement already exists')

class AnnView(MethodView):

    def get(self, ann_id = None):
        if ann_id is None:
            announcements = request.session.query(Ann).all()
            return jsonify([a.dict for a in announcements])
        else:
            announcement = get_ann_by_id(ann_id)
            return jsonify(announcement.dict)

    def post(self):
        json_data = validate_json(request.json, AnnouncementCreate)
        announcement = Ann(
            title=json_data['title'],
            descr=json_data['descr'],
            owner=json_data['owner']
        )
        add_ann(announcement)
        return jsonify(announcement.dict)

    def patch(self, ann_id):
        json_data = validate_json(request.json, AnnouncementUpdate)
        announcement = get_ann_by_id(ann_id)
        if 'title' in json_data:
            announcement.title = json_data['title']
        if 'descr' in json_data:
            announcement.descr = json_data['descr']
        if 'owner' in json_data:
            announcement.owner = json_data['owner']
        add_ann(announcement)
        return jsonify(announcement.dict)

    def delete(self, ann_id):
        announcement = get_ann_by_id(ann_id)
        request.session.delete(announcement)
        request.session.commit()
        return jsonify({'message': 'Announcement deleted'})

ann_view = AnnView.as_view('ann_view')
app.add_url_rule('/api/v1/announcements', view_func=ann_view, methods=['POST', 'GET'])
app.add_url_rule('/api/v1/announcements/<int:ann_id>', view_func=ann_view,
                 methods=['GET', 'PATCH', 'DELETE'])
app.run()
