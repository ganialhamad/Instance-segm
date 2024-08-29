const weeks = [1, 2, 3, 4, 5, 6, 7]
const inCommingBookings = API_obj.bookings

for (const idx, booking in inCommingBookings) {
  if (booking.date == weeks[idx]) {
    console.log("Logged: ", booking.date, booking.time);
  }
}
