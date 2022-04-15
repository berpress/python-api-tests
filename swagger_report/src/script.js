const app = () => {
  const state = {
    all: [],
    success: [],
    failed: [],
    notAdd: []
  };

  const accordions = document.querySelectorAll('.accordion-item');
  const allButton = document.querySelector('#all');
  const successButton = document.querySelector('#success');
  const failedButton = document.querySelector('#not-checked');
  const notAddButton = document.querySelector('#not-added');
  const accordionsDiv = document.querySelector('#accordions');


  state.all = accordions;

  const findStatusElement = (item, color) => {
    const button = item.querySelector('.accordion-header').querySelector('button');
    const status = button.getAttribute('style');
    if (status === `background-color: ${color};`) {
      return item;
    }
  }

  state.success = Array.from(accordions).filter((item) => {
    return findStatusElement(item, '#60d891')
  })


  state.failed = Array.from(accordions).filter((item) => {
    return findStatusElement(item, '#F47174')
  })

  state.notAdd= Array.from(accordions).filter((item) => {
    return findStatusElement(item, '#F56b02')
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

  allButton.addEventListener('click', () => { showItems(state.all);});
  successButton.addEventListener('click', () => { showItems(state.success);});
  failedButton.addEventListener('click', () => { showItems(state.failed);});
  notAddButton.addEventListener('click', () => { showItems(state.notAdd);});
  const accordionArray = Array.from(document.getElementsByClassName('accordion-button'));
  accordionArray.forEach(el => el.addEventListener('click', showBtnHandler));
}

app();
