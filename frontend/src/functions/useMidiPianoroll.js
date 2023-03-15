


const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

export const createVerticalKeyboard = (id,height, width,paddingRight, colors) => {

  const pianoroll = document.getElementById(`pianoroll-${id}`)
  const svgElements = pianoroll.querySelector(`div:nth-of-type(3) svg`);
  pianoroll.getElementsByTagName('div')[2].style.paddingRight = `${paddingRight}px`
  
  const notes = Array.from(svgElements.querySelectorAll('.note'));
  const pitches = notes.map(note => Number(note.getAttributeNS(null, 'data-pitch'))); // získání všech hodnot 'data-pitch' jako pole čísel
  const maxMidiNumber = Math.max(...pitches)
  const minMidiNumber = Math.min(...pitches)


    const pitchAccidentals = {};
    for (let i = minMidiNumber; i <= maxMidiNumber; i++) {
        const hasAccidentalNote = hasAccidental(i); 
        pitchAccidentals[i] = hasAccidentalNote;
    }

  const numOfKeys = Object.keys(pitchAccidentals).length;
  const keyHeight = Math.round(height / numOfKeys)
  pianoroll.config = {pixelsPerTimeStep: width, noteHeight: keyHeight}

 
  const keyboard = document.createElement("div");
  keyboard.style.display = "flex";
  keyboard.style.flexDirection = "column";
  keyboard.style.height = (numOfKeys * keyHeight) + "px";
  keyboard.style.width = 40 + "px";
  keyboard.style.marginTop = keyHeight * 2 + "px"; //there is margin because of visualization


  const keyboardDiv = document.getElementById(`keyboard-${id}`)
  if (keyboardDiv.hasChildNodes()) {
    keyboardDiv.removeChild(keyboardDiv.firstChild);
  }
  
  let currentMaxMidiNumber = maxMidiNumber
  while (currentMaxMidiNumber >= minMidiNumber) {
  const key = document.createElement("div");
  key.style.flexGrow = 1;
  key.style.height = keyHeight + "px";
  key.style.borderBottom = "1px solid gray ";
  key.style.borderRight = "1px solid gray ";
  key.id = `key-${currentMaxMidiNumber}`
  keyboard.appendChild(key);


  if(!pitchAccidentals[currentMaxMidiNumber]){
      
      key.classList.add('white-background');
  } else {
      key.classList.add('black-background');
  } 
  
  if(['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7'].includes(getNoteName(currentMaxMidiNumber)) || (currentMaxMidiNumber == maxMidiNumber) || (currentMaxMidiNumber == minMidiNumber)){
    createKeyDescription(key,keyHeight,currentMaxMidiNumber  )
  }

  currentMaxMidiNumber--
  }

  document.getElementById(`keyboard-${id}`).appendChild(keyboard);


  if(colors){
    setTimeout(() => {
      colors.forEach((color, index) => {
        setInstrumentColor(id, index, color)
      
      });
      
    }, 1000);

  }
  return false
}
// const setSize = (size) => {

//   pianoroll.config = {noteHeight: size/(maxMidiNumber-minMidiNumber)}

// }
export const setInstrumentColor = (id, numberOfInstrument, color) => {

  const pianoroll = document.getElementById(`pianoroll-${id}`)
  var svg = pianoroll.getElementsByTagName('div')[2].getElementsByTagName('svg')[0];
  const notes = Array.from(svg.querySelectorAll('.note'));
  const instruments = notes.map(note => Number(note.getAttributeNS(null, 'data-instrument')))
  const uniqueInstruments = Array.from(new Set(instruments));
  const instrumentColors = {};

  if(color){
    notes.forEach((element, id) => {
        if(instruments[id] == numberOfInstrument){
        
            element.setAttributeNS(null, 'fill', color)
        }
    });
 }

 uniqueInstruments.forEach(instrumentId => {
  const instrumentNotes = notes.filter(note => Number(note.getAttributeNS(null, 'data-instrument')) === instrumentId);
  const instrumentColor = instrumentNotes.length > 0 ? instrumentNotes[0].getAttributeNS(null, 'fill') : null;
  instrumentColors[instrumentId] = instrumentColor;
});

  return {uniqueInstruments, instrumentColors}
}

function hasAccidental(midiNumber) {
  const noteName = noteNames[midiNumber % 12];
  return noteName.includes('#') || noteName.includes('b');
}

function getNoteName(midiNumber) {
  const octave = Math.floor(midiNumber / 12) - 1;
  const noteName = noteNames[midiNumber % 12];
  return noteName + octave;
 }

const createKeyDescription = (key, keyHeight, currentMaxMidiNumber) => {
  const text = document.createElement("div");
  text.style.height = keyHeight + "px";
  text.textContent = getNoteName(currentMaxMidiNumber)
  text.id = 'noteName'
  text.style.marginLeft = '41px'
  text.style.marginTop = '-10px'
  text.style.position = 'absolute'
  text.style.fontSize = '12px'
  text.style.color = 'red'
  key.appendChild(text)
}




export const trackCursorPosition = (wavePos, id, dynamicNames) => {
  const matchingKeys = [];
  const pianoroll = document.getElementById(`pianoroll-${id}`)
  const svgElements = pianoroll.querySelector(`div:nth-of-type(3) svg`);
  const note = Array.from(svgElements.querySelectorAll('.note'));
  const keyboardElements = document.getElementById(`keyboard-${id}`).querySelectorAll('[id*="key"]')

  //set border of each note, which is hit by cursor
  for (let i = 0; i < note.length; i++) {
    let element = note[i];
    let startTime = element.x.baseVal.value
    let endTime = element.x.baseVal.value + element.width.baseVal.value
    if (wavePos >= startTime && wavePos < endTime) {

      const keyId = parseInt(element.getAttributeNS(null, 'data-pitch'));
      matchingKeys.push(keyId);
      element.setAttributeNS(null, 'stroke', 'red');
      element.setAttributeNS(null, 'stroke-width', '2');

    } else {
        element.removeAttributeNS(null, 'stroke');
    }
  }   
  //set color of each key

  for (let i = 0; i < keyboardElements.length; i++) {
    const keyId = parseInt(keyboardElements[i].id.split("-")[1]);
    // if(!dynamicNames){
    //   keyboardElements[i].innerHTML = "";
    //   if(['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7'].includes(getNoteName(keyId))){
    //     createKeyDescription(keyboardElements[i],7, keyId)
    //   }
    // }

    if (matchingKeys.includes(keyId)) {
        keyboardElements[i].style.backgroundColor = 'red';
        if(dynamicNames){
          createKeyDescription( keyboardElements[i],7, keyId)
        }
    } else {
        keyboardElements[i].style.backgroundColor = '';
        if(dynamicNames){
          keyboardElements[i].innerHTML = "";
        }

    }
}




}

