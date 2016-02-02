import twist


class Protocol(object):
  def __init__(self, funct):
    self.__funct = funct
  
  def __call__(self, *args, **kwargs):
    print('test')


class JsonProtocol(twist.Protocol):
  def read(self):
    from json import loads
    try:
      self.request.json = loads(self.request.body)
    except:
      self.request.json = None
  
  def write(self, returned):
    from json import dumps
    self.response.headers('Content-Type', 'application/json')
    self.response.write(dumps(returned, indent=2))


class ErrorProtocol(twist.Protocol):
  def __init__(self, errormap):
    self.errors = errormap
  
  def execute(self, funct):
    try:
      return funct(self.request, self.response)
    except Exception as error:
      if not error in self.errors:
        return {'success':False, 'code':-1, 'message':'Unknown Server Error'}
      else:
        errorTuple = self.errors[error]
        return {'success':False, 'code':errorTuple[0], 'message':errorTuple[1]}
  
  def write(self, returned):
    if not 'success' in returned:
      returned['success'] = True
    return returned


api = twist.api(debug=True, protocol=(JsonProtocol, ErrorProtocol))


@api.post('/api/login/?')
def LoginUser(request, response):
  url = request.url()
  key = url.parametes('key')
  
  json = request.json
  userid, postid = json.parameters('userid', 'postid')
  Link.vote(userid, postid)
  
  response.headers['Content-Type'] = 'application/json'
  response.headers('Content-Type', 'application/json')
  
  return { 'success': True }


@api.get('/.*')
def MainHandler(request, response):
  response.out.template('main', posts=Post.queryAll())


api.serve()