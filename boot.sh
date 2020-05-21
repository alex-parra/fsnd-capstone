
case $1 in
  dev) FLASK_ENV=development flask run --reload ;;
  test) python -m unittest -v test_app.py ;;
  *) echo "Unknow command"
esac
