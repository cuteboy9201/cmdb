import logging

from oslo.form.fields import BoolField, EmailField, IntegerField, StringField, StringListField
from oslo.form.form import Form


class BasePostForm(Form):
    def __init__(self, handler=None):
        self.authInfo = StringField(required=False)
        self.connectHost = StringField(required=True)
        self.connectPort = IntegerField(required=True)
        self.desc = StringField(required=True)
        self.env = StringField(required=True)
        self.name = StringField(required=True)
        super(BasePostForm, self).__init__(handler=handler)


class GETBaseForm(Form):
    def __init__(self, handler=None):
        self.pageIndex = IntegerField(required=True)
        self.pageSize = IntegerField(required=True)
        self.sortBy = StringField(required=False)
        self.descending = BoolField(required=True)
        self.name = StringField(required=False)
        super(GETBaseForm, self).__init__(handler=handler)


class PUTBaseForm(Form):
    def __init__(self, handler=None):
        # self.id = StringField(required=True)
        self.authInfo = StringField(required=False)
        self.connectHost = StringField(required=True)
        self.connectPort = IntegerField(required=True)
        self.desc = StringField(required=True)
        self.env = StringField(required=True)
        self.name = StringField(required=True)
        super(PUTBaseForm, self).__init__(handler=handler)