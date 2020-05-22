
case $1 in
  db-up) docker-compose up -d ;;

  db-dn) docker-compose down ;;

  dev) FLASK_ENV=development flask run --reload ;;

  test) python -m unittest -v test_app.py ;;

  *) echo "Unknow command"
esac
