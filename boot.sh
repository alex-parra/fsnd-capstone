
case $1 in
  db-up) docker-compose up -d ;;

  db-dn) docker-compose down ;;

  dev) FLASK_ENV=development flask run --reload ;;

  test) FLASK_ENV=testing python test_app.py ;;

  *) echo "Unknow command"
esac
