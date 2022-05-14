const app = () => {
  const state = {
    all: [],
    success: [],
    failed: [],
    notAdd: [],
    search: [],
  };

  const accordions = document.querySelectorAll('.accordion-item');
  const allButton = document.querySelector('#all');
  const successButton = document.querySelector('#success');
  const failedButton = document.querySelector('#not-checked');
  const notAddButton = document.querySelector('#not-added');
  const accordionsDiv = document.querySelector('#accordions');
  const searchButton = document.querySelector('#search-button');
  const searchInput = document.querySelector('#search');


  state.all = accordions;

  const findStatusElement = (item, color) => {
    const button = item.querySelector('.accordion-header').querySelector('button');
    const status = button.getAttribute('style');
    if (status === `background-color: ${color};`) {
      return item;
    }
  }

  state.success = Array.from(accordions).filter((item) => {
    return findStatusElement(item, '#d6facf')
  })


  state.failed = Array.from(accordions).filter((item) => {
    return findStatusElement(item, '#f59993')
  })

  state.notAdd= Array.from(accordions).filter((item) => {
    return findStatusElement(item, '#f2b85a')
  })

  const showBtnHandler = (event) => {
    const element = event.target.parentNode.parentNode.children[1];
    const attribute = element.getAttribute("data-state");
    if (attribute === 'open') {
      element.setAttribute("data-state", "collapsed");
      element.setAttribute("class", "accordion-collapse collapse");
    } else {
      element.setAttribute("data-state", "open");
      element.setAttribute("class", "accordion-collapse open");
    }
  };

  const showItems = (items) => {
    accordionsDiv.innerText = '';
    Array.from(items).forEach(element => accordionsDiv.appendChild(element));
  }

  state.success = Array.from(accordions).filter((item) => {
    return findStatusElement(item, '#d6facf')
  })


  const searchItems = (events, items) => {
    events.preventDefault();
    Array.from(items).forEach(element => {
      if(element.innerText.indexOf(searchInput.value) !== -1)
        {
          state.search.push(element);
          showItems(state.search);
          return true;
        }
    });
  }

  allButton.addEventListener('click', () => { showItems(state.all);});
  successButton.addEventListener('click', () => { showItems(state.success);});
  failedButton.addEventListener('click', () => { showItems(state.failed);});
  notAddButton.addEventListener('click', () => { showItems(state.notAdd);});
  const accordionArray = Array.from(document.getElementsByClassName('accordion-button'));
  accordionArray.forEach(el => el.addEventListener('click', showBtnHandler));
  searchButton.addEventListener('click', (e) => { searchItems(e, state.all);});
  searchInput.addEventListener('click', () => { showItems(state.all);});
}

app();
