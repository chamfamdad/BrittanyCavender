showSlides('no_key');

function showSlides(key) {
  // clear out the current
  let slideshow = document.getElementById("slideshow")
  slideshow.replaceChildren()

  // load up the selected key
  fetch(key + '.json')
    .then(response => response.json())
    .then(data => {
      console.log(data);

      h2 = document.createElement('h2');
      h2.textContent = data.key.length > 0 ? data.key : 'Not Labeled';
      h2.setAttribute("class", 'text-center')
      slideshow.appendChild(h2);

      i = 1;
      total = data.images.length
      data.images.forEach(element => {
        slides = document.createElement('div');
        slides.setAttribute('class', 'container p-2');

        card = document.createElement('div');
        card.setAttribute('class', 'card');
        
        img = document.createElement('img');
        img.src = './' + element.source;
        img.style = 'width:100%';
        img.alt = element.caption;
        img.setAttribute('class', 'card-img-top');
        card.appendChild(img);
             
        cardBody = document.createElement('div');
        cardBody.setAttribute('class', 'card-body container');

        row = document.createElement('div');
        row.setAttribute('class', 'row');

        cardBody.appendChild(row);

        caption = document.createElement('div');
        caption.setAttribute('class', 'col');
        caption.textContent = element.caption;

        row.appendChild(caption);

        count = document.createElement('div');
        count.setAttribute('class', 'col text-end');
        count.textContent = i + ' / ' + total;

        row.appendChild(count);

        card.appendChild(cardBody);
        slides.appendChild(card)

        slideshow.appendChild(slides);

        console.log('added', element)

        i++;
      });
    })
    .catch(error => {
      // Handle any errors
      console.error('Error:', error);
    });
}  
