# Example workflow

Metro is a big music fan and likes to be on top of every new song from his favorite artists. He wants to be able to add a song into the data base if it hasn't been added. He will start by gathering all the information from the particular song. This includes the song name, artist(s) name, album name, and other important information. Then Metro will send the information to the data base. Lastly, he will get a response on whether the song was successfully added or if it already exists.

# Testing results

<Repeated for each step of the workflow>
1. The curl statement called. You can find this in the /docs site for your 
API under each endpoint. For example, for my site the /catalogs/ endpoint 
curl call looks like:
curl -X 'GET' \
  'https://centralcoastcauldrons.vercel.app/catalog/' \
  -H 'accept: application/json'
2. The response you received in executing the curl statement.
