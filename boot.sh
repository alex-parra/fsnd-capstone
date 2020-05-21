
case $1 in
  dev) FLASK_ENV=development python app.py ;;
  *) echo "Unknow command"
esac
