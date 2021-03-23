class Config:
    SQLALCHEMY_DATABASE_URI = 'oracle+cx_oracle://feishui:123456@192.169.1.121/cdzydw'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ENGINE_OPTIONS = "encoding = 'UTF-8'"
