import twist


api = twist.api(debug=True)


api.post('/api/login/?')
def LoginUser(request, response):
  json = request.json()
  userid, postid = json.parameters('userid', 'postid')
  Link.vote(userid, postid)
  return {
    'success': True
  }


api.get('/.*')
def MainHandler(request, response):
  response.out.template('main', posts=Post.queryAll())


api.serve()