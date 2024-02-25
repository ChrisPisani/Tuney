from wtforms import Form, StringField, SelectField, validators

class Song_search(Form):
    choices = [('Song Name', 'Song Name'),
               ('Song Name & Artist', 'Song Name & Artist')]
    select = SelectField('Search By:', choices=choices)
    # Client side validation before searching
    song_string = StringField(u'Song Name', validators=[validators.InputRequired(),validators.Length(min=1, max=20)], render_kw={"placeholder": "Required"})
    artist_string = StringField(u'Artist Name', validators=[validators.Length(min=1, max=20)], render_kw={"placeholder": "Optional"})
