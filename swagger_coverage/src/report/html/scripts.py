JS_SCRIPT = """
<script type="text/javascript">
const app = () => {
  const state = {
    all: [],
    success: [],
    failed: [],
    notAdd: [],
    partial: [],
    search: [],
  };

  const allButton = document.querySelector('#all');
  const successButton = document.querySelector('#checked');
  const failedButton = document.querySelector('#not_checked');
  const notAddButton = document.querySelector('#not_added');
  const partialCheckedButton = document.querySelector('#partial_checked');
  const example = document.querySelector('#accordionFlushExample');

  const findStatusElement = (item, status) => {
    if (item.tagName === 'H3') {
      return item;
    }
    const button = item.querySelector('.accordion-header').querySelector('button');
    const findStatus = button.getAttribute('data-status');
    if (findStatus === status) {
      return item;
    }
  }

  state.success = Array.from(example.children).filter((item) => {
    return findStatusElement(item, 'checked')
  })


  state.failed = Array.from(example.children).filter((item) => {
    return findStatusElement(item, 'not_checked')
  })

  state.notAdd= Array.from(example.children).filter((item) => {
    return findStatusElement(item, 'not_added')
  })

  state.partial= Array.from(example.children).filter((item) => {
    return findStatusElement(item, 'partially_checked')
  })

  state.all = Array.from(example.children, item => item);


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
    example.innerText = '';
    Array.from(items).forEach(element => example.appendChild(element));
  }



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
  partialCheckedButton.addEventListener('click', () => { showItems(state.partial);});
  const accordionArray = Array.from(document.getElementsByClassName('accordion-button'));
  accordionArray.forEach(el => el.addEventListener('click', showBtnHandler));
}

app();

</script>
"""
