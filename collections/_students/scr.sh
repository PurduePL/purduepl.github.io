for n in *

do
  mv $n $(echo $n | sed -e 's/.*-//')
done
