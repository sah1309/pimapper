<?php
/**
 * web -- OauthAbstract.php
 * User: Simon Beattie
 * Date: 19/12/2013
 * Time: 00:35
 */


class StatusAbstract
{

    /**
     * @var object $oauth
     */
    protected $oauth;

    public function __construct(array $oauth)
    {
        $this->setOauth($oauth);

    }

    /**
     * getConfig returns the config from the object
     *
     * @return array
     */
    public function getConfig()
    {
        return $this->oauth;
    }

    /**
     * setPdo sets the pdo property in object storage
     *
     * @param \PDO $pdo
     * @throws InvalidArgumentException
     * @return StatusAbstract
     */
    public function setOauth($pdo)
    {
        if (empty($oauth))
        {
            throw new \InvalidArgumentException(__METHOD__ . ' cannot accept an empty Oauth object');
        }
        $this->oauth = $oauth;
        return $this;
    }

    /**
     * getPdo returns the pdo from the object
     *
     * @return \PDO
     */
    public function getOauth()
    {
        return $this->oauth;
    }

}