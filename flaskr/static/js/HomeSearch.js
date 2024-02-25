function onSelectChange()
{
  if (search_select.selectedIndex === 0)
  {
    $('[for="artist_string"]').css('display','none')
    artist_name.style.display = 'none'
  }
  else if (search_select.selectedIndex === 1)
  {
    $('[for="artist_string"]').css('display','inline-block')
    artist_name.style.display = 'inline-block'
  }
}

let song_name = document.getElementById('song_string')
let artist_name = document.getElementById('artist_string')
let search_select = document.getElementById('select')

artist_name.style.display = 'none'
$('[for="artist_string"]').css('display','none')

search_select.addEventListener('change', onSelectChange, false)
