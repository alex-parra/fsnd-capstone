
case $1 in
  dev) FLASK_ENV=development flask run --reload ;;
  *) echo "Unknow command"
esac
