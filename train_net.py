const weeks = [1, 2, 3, 4, 5, 6, 7]
const inCommingBookings = API_obj.bookings

for (const idx, booking in inCommingBookings) {
  if (booking.date == weeks[idx]) {
    console.log("Logged: ", booking.date, booking.time);
  }
}


// interval time & duration

for (let i = 0; i < inCommingBookings.length; i++) {
  const { id, time, duration } = inComingBookings[i];
  const time = document.getElementById('time-picked')
  const duration = document.getElementById('duration-picked')

  const start_booking_time = time;
  const end_booking_time = (duration / 60) * 60000;

  if () {}
}
